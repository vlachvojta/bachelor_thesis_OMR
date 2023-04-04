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

rel_dir = os.path.dirname(os.path.relpath(__file__))
sys.path.append(os.path.join(rel_dir, '..', 'dataset-utilities'))
from common import Common  # noqa: E402


class Matchmaker:
    """Get label-image pairs from two separate folders."""
    def __init__(self, label_files: list, image_folder: list = ['.'],
                 output_folder: str = 'pairs', verbose: bool = False):
        self.label_files = label_files
        self.image_folder = image_folder
        self.output_folder = output_folder
        self.verbose = verbose
        self.stats_file = os.path.join(self.output_folder, '0_stats.json')
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
            print("ERROR: No images or labels where found, cannot generate no match.")
            return

        images_base = [os.path.basename(image) for image in self.images]

        image_parts = [self.get_part_name_with_suspicious(img) for img in images_base]
        label_parts = [self.get_part_name(label) for label in self.labels]

        image_parts = self.list_to_dict_sum(image_parts)
        label_parts = self.list_to_dict_sum(label_parts)

        print(f'LABELS originate from {len(label_parts)} parts.')
        print(f'IMAGES originate from {len(label_parts)} parts.')

        self.get_stats_about_parts(image_parts, label_parts)

        sus_img_parts = self.get_sus_parts(images_base)  # - self.extra_image_parts
        # print(f'\t{len(sus_img_parts)} part(s) has generated suspicious images.')
        logging.debug(f'sus parts: {sus_img_parts}')

        logging.debug('---- Finding complete parts: ----')
        logging.debug('----(printing only incomplete)---')
        complete_parts = self.get_complete_parts(image_parts, label_parts, sus_img_parts)

        self.print_results(complete_parts, sus_img_parts)

        self.copy_complete_parts(complete_parts)

    def copy_complete_parts(self, complete_parts):
        """Copy complete parts of labels and images to given location and rename them to match."""

        # Find all complete parts images with path to source image
        print("Getting images with path")
        startos = time.time()
        images_with_path = self.get_images_with_path(complete_parts)
        endos = time.time()
        print(f'Time looking for images: {endos - startos:.2f} s')

        print("Getting labels with path")
        startos = time.time()
        complete_labels = self.get_complete_labels(complete_parts)
        endos = time.time()
        print(f'Time looking for images: {endos - startos:.2f} s')

        self.save_labels(complete_labels)

        assert len(images_with_path) == len(complete_labels),\
            "Length of complete images and labels is not equal."

        # complete_parts_subset = {}
        # complete_parts_subset["1003231_p00"] = complete_parts["1003231_p00"]

        if self.verbose:
            print(f'Labels saved, copying images from {len(complete_parts)} parts.')
        else:
            print(f'Labels saved, copying images from {len(complete_parts)} parts '
                  '(every dot is 200 images, line is 10_000)')

        for i, (complete_part, pairs_count) in enumerate(complete_parts.items()):
            if not self.verbose:
                Common.print_dots(i, 200, 10_000)
            logging.debug(f"Copying {complete_part}")
            image_with_path = images_with_path[complete_part]
            part_labels = complete_labels[complete_part]

            if not pairs_count == len(image_with_path):
                print(f"Part {complete_part} couldn't be copied, because of len of images error. SKIPPING "
                      f"Should have {pairs_count} but got {len(image_with_path)} instead")
                continue

            if not pairs_count == len(part_labels):
                print(f"Part {complete_part} couldn't be copied, because of len of labels error. SKIPPING")
                continue

            for label_id, image_with_path in zip(sorted(part_labels),
                                                 image_with_path):
                output_image = os.path.join(self.output_folder, f'{label_id}.png')
                copyfile(image_with_path, output_image)
                # logging.debug(f'{label_id} {image_with_path} => {output_image}')
        print()

        print(f"Copying successfull to {self.output_folder}, labels saved to {self.out_label_file}")

    def get_complete_labels(self, complete_parts) -> dict:
        """Get part names and find all labels that originate from every part.

        Return dictionary, key: part name, value: dict of labels (labe_id, label)
        """
        complete_parts_keys = list(complete_parts.keys())

        complete_labels = {}
        for part_id in complete_parts_keys:
            results = {label_id: label for label_id, label in self.labels.items()
                       if f"{part_id}_" in label_id}

            if len(results) > 0:
                complete_labels[part_id] = results

        return complete_labels

    def get_images_with_path(self, complete_parts) -> dict:
        """Get complete parts name and find all input images that originate from this part.
        
        Return dictionary, key: part name, value: list of image names with paths.
        """
        complete_parts_keys = list(complete_parts.keys())

        images_with_path = {}
        for part_id in complete_parts_keys:
            finder = re.compile(f".*{part_id}[_-].*")
            found_images = list(filter(finder.match, self.images))

            if len(found_images) > 0:
                images_with_path[part_id] = found_images

        return images_with_path

    def save_labels(self, complete_labels) -> None:
        """Flatten dictionary of dictionary of labels and save to a file."""
        # Flatten dictionary
        labels_db = {}
        for part, labels_in_part in complete_labels.items():
            if isinstance(labels_in_part, dict):
                labels_db.update(labels_in_part)
            else:
                logging.warning("Value of label_db is not a dict, "
                                f"possible loss of labels for part {part}")

        # Save labels to a file
        label_output_lines = [f'{file}.png {Common.PERO_LMDB_zero_tag} {labels}'
                              for file, labels in labels_db.items()]
        output = '\n'.join(sorted(label_output_lines)) + '\n'
        Common.write_to_file(output, self.out_label_file)

    def print_results(self, complete_parts, sus_img_parts):
        print('')
        print('--------------------------------------')
        print('Results:')
        total_parts_found_len = len(self.total_parts_found)
        print(f'From total {total_parts_found_len} unique parts found:')

        complete_parts_len = len(complete_parts)
        complete_ratio = complete_parts_len / total_parts_found_len * 100
        self.sum_values = sum(complete_parts.values())
        print(f'\t{complete_parts_len} ({complete_ratio:.1f} %) complete parts with '
              f'{self.sum_values} images and labels.')

        no_new_system_len = len(self.no_new_system_parts)
        no_new_system_ratio = no_new_system_len / total_parts_found_len * 100
        print(f'\t{no_new_system_len} ({no_new_system_ratio:.1f} %) parts '
              'generated only one label and more images. (missing new-system tag in musicxml)')

        not_fit_len = len(self.not_fitting_staff_parts)
        not_fit_ratio = not_fit_len / total_parts_found_len * 100
        print(f'\t{not_fit_len} ({not_fit_ratio:.1f} %) parts '
              'had differenct counts of labels and images.')

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
        output['Total parts found'] = list(self.total_parts_found)
        output['Complete parts len'] = complete_parts_len
        output['Complete parts'] = complete_parts
        output['No new system parts count'] = no_new_system_len
        output['No new system parts (image count)'] = self.no_new_system_parts
        output['Not fitting staff count'] = not_fit_len
        output['Not fitting staff parts (labels, images)'] = self.not_fitting_staff_parts
        output['Extra image parts count'] = extra_image_parts_len
        output['Extra image parts'] = list(self.extra_image_parts)
        output['Extra label parts count'] = extra_label_parts_len
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

    def get_complete_parts(self, image_parts: dict, label_parts: dict, sus_img_parts: set):
        """Go through images dictionary and labels dictionary and return complete parts.

        Part is complete when the number of images is equal to the number of labels and 
        part has not generated any suspicious images."""
        complete_parts = {}

        for part_name, _ in image_parts.items():
            if (part_name in label_parts and
                    not part_name in sus_img_parts):
                if label_parts[part_name] == image_parts[part_name]:
                    # logging.debug(f'{part_name}:\t(i: {image_parts[part_name]},'
                    #               f' l: {label_parts[part_name]})\tOK')
                    complete_parts[part_name] = label_parts[part_name]
                elif label_parts[part_name] == 1:
                    self.no_new_system_parts[part_name] = image_parts[part_name]
                else:
                    self.not_fitting_staff_parts[part_name] = [label_parts[part_name],
                                                               image_parts[part_name]]
                    logging.debug(f'{part_name}:\t(i: {image_parts[part_name]},'
                                  f' l: {label_parts[part_name]})\t')

        return complete_parts

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
            labels[system_id] = ' '.join(sequence)

        return labels

    def get_sus_parts(self, images: list) -> set:
        """Get a list of images in input folders, return onlysuspicious images.
        
        Suspicious image name starts with 'z'."""
        # print(images)
        # all_images = [os.path.basename(image) for image in self.images]

        sus_parts = set()
        for image in images:
            if image[0] == 'z':
                _, file_name, part_name, *_  = re.split(r'\_|\-', image)
                sus_parts.update(['_'.join([file_name, part_name])])

        return sus_parts


    def get_part_name(self, file: str):
        """Get file name, return part name."""
        mscz_id, part_id, *_ = re.split(r'_|-', file)
        # print(f'mscz: {mscz_id}, part: {part_id}, rest: {rest}')

        return f'{mscz_id}_{part_id}'

    def get_part_name_with_suspicious(self, file: str):
        """Get file name, return part name."""
        if file[0] == 'z':
            _, mscz_id, part_id, *_ = re.split(r'_|-', file)
        else:
            mscz_id, part_id, *_ = re.split(r'_|-', file)
        # print(f'mscz: {mscz_id}, part: {part_id}, rest: {rest}')

        return f'{mscz_id}_{part_id}'

    def list_to_dict_sum(self, parts: list) -> dict:
        """Get list with duplicate values, return sum of occurences in dict."""
        sums = {}
        processed_parts = set()

        for part in parts:
            if part in processed_parts:
                sums[part] += 1
            else:
                processed_parts.add(part)
                sums[part] = 1
        return sums


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
