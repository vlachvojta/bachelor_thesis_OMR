#!/usr/bin/python3.8
"""Get label-image pairs from two folders and copy to a new folder with corresponding names.

Part is complete when the number of images is equal to the number of labels and
part has not generated any suspicious images.

Image is suspicious when a whole page image was split
into images higher then threshold = it's not an image of one music stave but more.
In the input folder this is said by the image name starting with 'z'.

Usage:
$ python3 matchmaker.py --labels 5_labels/generated_labels.semantic --images 4_images -o 6_pairs
Resulting in copying pairs of labels and images to 6_pairs with new names.
"""

import argparse
import re
import sys
import os
import time
import logging
from shutil import copyfile
from datetime import datetime

rel_dir = os.path.dirname(os.path.relpath(__file__))
sys.path.append(os.path.join(rel_dir, '..', 'dataset-utilities'))
from common import Common  # noqa: E402


class Matchmaker:
    """Get label-image pairs from two separate folders."""
    def __init__(self, label_files: list = None, image_folder: list = None,
                 output_folder: str = 'pairs', verbose: bool = False):
        self.label_files = label_files if label_files else []
        self.image_folder = image_folder if image_folder else []
        self.output_folder = output_folder
        self.verbose = verbose
        self.stats_file = os.path.join(self.output_folder, '0_matchmaker_stats.json')
        self.out_label_file = os.path.join(self.output_folder, '0_labels.semantic')

        if verbose:
            logging.basicConfig(level=logging.DEBUG, format='[%(levelname)-s]\t- %(message)s')
        else:
            logging.basicConfig(level=logging.INFO,format='[%(levelname)-s]\t- %(message)s')

        # Load labels
        print(f'Loading labels from {len(self.label_files)} files.')
        self.labels = {}
        for label_file in label_files:
            self.labels.update(self.load_labels(label_file))
        if not self.labels:
            print('WARNING: No valid LABELS in given folder.')
        else:
            print(f'\tFound {len(self.labels)} labels.')

        # Load images from folders
        self.images = []
        sub_folders = [os.path.join(self.image_folder, folder)
                       for folder in os.listdir(self.image_folder)]
        image_folders = [folder for folder in sub_folders if os.path.isdir(folder)]
        image_folders += [self.image_folder]
        print(f'Looking for images in {len(image_folders)} folders '
              '(including the root input folder)')

        for image_folder in image_folders:
            self.images += Common.listdir(image_folder, ['png'])
        if not self.images:
            print('WARNING: No valid IMAGES in given folder.')
        else:
            print(f'\tFound {len(self.images)} image files.')

        # Create output part if necessary
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        self.no_new_system_parts = {}
        self.not_fitting_staff_parts = {}
        self.total_parts_found = set()
        self.extra_label_parts = set()
        self.extra_image_parts = set()
        self.sum_values = 0

    def __call__(self):
        if not self.images or not self.labels:
            logging.error("No images or labels were found, cannot generate no match.")
            return

        image_parts = self.aggregate_files_to_parts(self.images)
        label_parts = self.aggregate_files_to_parts(self.labels)

        self.get_stats_about_parts(image_parts, label_parts)

        print(f'LABELS originate from {len(label_parts)} parts.')
        print(f'IMAGES originate from {len(image_parts)} parts.')
        print(f'TOTAL  unique parts:  {len(self.total_parts_found)}.')

        # select parts that both generated some labels and images
        sus_img_parts = [part_name for part_name, part_data in image_parts.items()
                         if part_name in label_parts and part_data['sus']]
        logging.debug(f'sus parts: {sus_img_parts}')
        logging.debug('---- Finding complete parts: ----')
        logging.debug('----(printing only incomplete)---')

        complete_parts = self.get_complete_parts(image_parts, label_parts)
        self.print_results(complete_parts, sus_img_parts)
        self.copy_complete_parts(complete_parts)

    def copy_complete_parts(self, complete_parts):
        """Copy complete PAIRS of labels and images to given location and renamte them to match."""
        if os.path.exists(self.out_label_file):
            date = datetime.now().strftime("%Y_%m_%d_%H-%M-%S")
            self.out_label_file = os.path.join(self.output_folder, f'0_labels_{date}.semantic')
            print(f'PRINTING to new file with date as ID: {date}')

        if self.verbose:
            print(f'Copying images and labels from {len(complete_parts)} parts.')
        else:
            print(f'Copying images and labels from {len(complete_parts)} parts '
                  '(every dot is 200 parts, line is 1_000)')

        with open(self.out_label_file, 'w', encoding='utf-8') as out_label_file:
            for i, part_name in enumerate(sorted(complete_parts.keys())):
                if not self.verbose:
                    Common.print_dots(i, 200, 1_000)
                logging.debug(f"Copying {part_name}")

                for pair in complete_parts[part_name]:
                    # print(f"For ({pair['label_id']}) writing: {self.labels[pair['label_id']]}")
                    label_sequence = self.labels[pair['label_id']]
                    out_label_file.write(
                        f"{pair['label_id']}.png {Common.PERO_LMDB_zero_tag} {label_sequence}\n")

                    output_image = os.path.join(self.output_folder, f"{pair['label_id']}.png")
                    copyfile(pair['image_with_path'], output_image)
                    # print(f"{pair['label_id']} {pair['image_with_path']} => {output_image}")
        print()

        print(f"Copying successfull to {self.output_folder}, labels saved to {self.out_label_file}")

    def print_results(self, complete_parts, sus_img_parts):
        print('')
        print('--------------------------------------')
        print('Results:')
        total_parts_found_len = len(self.total_parts_found)
        print(f'From total {total_parts_found_len} unique parts found:')

        complete_parts_len = len(complete_parts)
        complete_ratio = complete_parts_len / total_parts_found_len * 100
        self.sum_values = sum([len(pairs) for pairs in complete_parts.values()])
        print(f'\t{complete_parts_len} ({complete_ratio:.1f} %) complete parts with '
              f'{self.sum_values} images and labels.')

        no_new_system_len = len(self.no_new_system_parts)
        no_new_system_ratio = no_new_system_len / total_parts_found_len * 100
        print(f'\t{no_new_system_len} ({no_new_system_ratio:.1f} %) parts '
              'generated only one label and more images. (missing new-system tag in musicxml)')

        not_fit_len = len(self.not_fitting_staff_parts)
        not_fit_ratio = not_fit_len / total_parts_found_len * 100
        print(f'\t{not_fit_len} ({not_fit_ratio:.1f} %) parts '
              'had different counts of labels and images.')

        sus_ratio = len(sus_img_parts) / total_parts_found_len * 100
        print(f'\t{len(sus_img_parts)} ({sus_ratio:.1f} %) parts generated suspicious images.')

        extra_image_parts_len = len(self.extra_image_parts)
        extra_image_ratio = extra_image_parts_len / total_parts_found_len * 100
        print(f'\t{extra_image_parts_len} ({extra_image_ratio:.1f} %) parts generated only images.')

        extra_label_parts_len = len(self.extra_label_parts)
        extra_label_ratio = extra_label_parts_len / total_parts_found_len * 100
        print(f'\t{extra_label_parts_len} ({extra_label_ratio:.1f} %) parts generated only labels.')

        output = {}
        output['Total parts found len'] = total_parts_found_len
        output['Complete parts len'] = complete_parts_len
        output['No new system parts count'] = no_new_system_len
        output['Not fitting staff count'] = not_fit_len
        output['Extra image parts count'] = extra_image_parts_len
        output['Extra label parts count'] = extra_label_parts_len
        output['Total parts found'] = list(self.total_parts_found)
        output['Complete parts'] = complete_parts
        output['No new system parts (image count)'] = self.no_new_system_parts
        output['Not fitting staff parts (labels, images)'] = self.not_fitting_staff_parts
        output['Extra image parts'] = list(self.extra_image_parts)
        output['Extra label parts'] = list(self.extra_label_parts)

        if not os.path.exists(self.stats_file):
            Common.write_to_file(output, self.stats_file)
            print(f'Stats saved to {self.stats_file}')
        else:
            print('WARNING: stats file already exists, printing to stdout.')
            print(output)

    def get_stats_about_parts(self, image_parts: dict, label_parts: dict) -> None:
        """Get stats about parts using dictionary input with names as keys. Save stats to self."""
        image_parts = set(image_parts.keys())
        label_parts = set(label_parts.keys())

        self.total_parts_found = image_parts.union(label_parts)
        self.extra_label_parts = label_parts - image_parts
        self.extra_image_parts = image_parts - label_parts

    def get_complete_parts(self, image_parts: dict, label_parts: dict) -> dict:
        """Go through images dictionary and labels dictionary and return complete parts.

        Part is complete when the number of images is equal to the number of labels and 
        part has not generated any suspicious images.

        Return dict
            key: part name
            value: list of pairs {'label_id': label id,
                                  'image_with_path': image with paths
        """
        complete_parts = {}

        for part_name, image_part_data in image_parts.items():
            if part_name in label_parts and not image_part_data['sus']:
                if label_parts[part_name]['count'] == image_part_data['count']:
                    pairs = self.get_system_id_image_pairs(image_part_data['files_with_paths'],
                                                           label_parts[part_name]['files'])
                    assert len(pairs) == image_part_data['count'], \
                           'ERROR in pairing system ids to images with paths'

                    complete_parts[part_name] = pairs
                elif label_parts[part_name]['count'] == 1:
                    self.no_new_system_parts[part_name] = part_name
                else:
                    self.not_fitting_staff_parts[part_name] = {
                        'label_count': label_parts[part_name]['count'],
                        'labels': label_parts[part_name]['files'],
                        'image_count': image_part_data['count'],
                        'images': image_part_data['files'],
                        'images_with_paths': image_part_data['files_with_paths'],
                    }
                    logging.debug(f'{part_name}:\t(i: {image_part_data["count"]},'
                                  f' l: {label_parts[part_name]["count"]})\t')
        return complete_parts

    def get_system_id_image_pairs(self, images_with_paths, label_ids) -> list:
        """Get system id pairs from a list of images with paths and label ids FROM ONE PART.
        
        Return list of dictionaries representing corresponding pairs.
        {'label_id': label id,
         'image_with_path': image file with path}
        """
        # Sort images with paths by file name and not folder name
        image_path_tuples = [(os.path.dirname(image), os.path.basename(image))
                             for image in images_with_paths]
        image_path_tuples.sort(key=lambda x: x[1])
        images_with_paths_sorted = [os.path.join(dir, image) for dir, image in image_path_tuples]

        assert len(images_with_paths) == len(label_ids), \
               'error in pairing while getting complete parts'

        pairs = []
        for label_id, image_with_path in zip(sorted(label_ids), images_with_paths_sorted):
            pairs.append({'label_id': label_id, 'image_with_path': image_with_path})

        return pairs

    def load_labels(self, filename: str) -> dict:
        """Load labels from file and return as a dictionary."""
        # print(f'labels file: {filename}')
        # print(f'path exists: {os.path.exists(filename)}')
        if not os.path.isfile(filename):
            return {}

        labels = Common.read_file(filename)

        if not labels:
            return {}

        labels_list = re.split(r'\n', labels)
        labels_list = list(filter(None, labels_list))   # filter out empty lines

        # print(type(labels_list))
        # print('len(labels_list): ')
        # print(len(labels_list))
        # print(labels_list[:10])

        labels = {}
        for label in labels_list:
            system_id, *sequence = re.split(r'\s', label)
            if system_id.endswith('.png'):
                labels[system_id[:-4]] = ' '.join(sequence)
            else:
                labels[system_id] = ' '.join(sequence)

        return labels

    def aggregate_files_to_parts(self, files_with_paths) -> dict:
        """Get list of files, aggregate them to dictionary of parts.

        Aggregate all files to parts, EVEN the ones with SUSPICIOUS names.

        Return dict:
            Keys: part_name
            Values: {'count': count of staves for given part,
                     'files': list of unique img files,
                     'files_with_paths': list of files with corresponding path,
                     'sus': True if some of part images are sus}."""
        parts_aggregated = {}

        for file_with_path in files_with_paths:
            file = os.path.basename(file_with_path)
            part_name = self.get_part_name(file)
            if not part_name:
                continue

            if not part_name in parts_aggregated:
                parts_aggregated[part_name] = {
                    'count': 1, 'files': [file], 'files_with_paths': [file_with_path],
                    'sus': file.startswith('z')}
            else:
                # check if file is NOT already in dict from different folder or something
                if not file in parts_aggregated[part_name]['files']:
                    parts_aggregated[part_name]['count'] += 1
                    parts_aggregated[part_name]['files'].append(file)
                    parts_aggregated[part_name]['files_with_paths'].append(file_with_path)
                    parts_aggregated[part_name]['sus'] |= file.startswith('z')

        return parts_aggregated

    def get_part_name(self, file: str):
        """Get file name, return part name. If file starts with 'z', return ''."""
        if file[0] == 'z':
            _, mscz_id, part_id, *_ = re.split(r'_|-', file)
        else:
            mscz_id, part_id, *_ = re.split(r'_|-', file)

        return f'{mscz_id}_{part_id}'


def parseargs():
    """Parse arguments."""
    print('sys.argv: ')
    print(' '.join(sys.argv))
    print('--------------------------------------')

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--image-folder", default='.',
        help="Input folder where to look for images and sub-folders with images.")
    parser.add_argument(
        "-l", "--label-files", nargs='+',
        help="Files with labels.")
    parser.add_argument(
        "-o", "--output-folder", type=str, default='pairs',
        help="Output folder to copy complete pairs.")
    parser.add_argument(
        '-v', "--verbose", action='store_true', default=False,
        help="Activate verbose logging.")
    return parser.parse_args()


def main():
    """Main function for simple testing"""
    args = parseargs()

    start = time.time()

    cutter = Matchmaker(
        image_folder=args.image_folder,
        label_files=args.label_files,
        output_folder=args.output_folder,
        verbose=args.verbose)
    cutter()

    end = time.time()
    print(f'Total time: {end - start:.2f} s')


if __name__ == "__main__":
    main()
