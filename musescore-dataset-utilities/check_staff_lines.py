import os
import sys
import cv2
import argparse
import numpy as np
from enum import Enum


rel_dir = os.path.dirname(os.path.relpath(__file__))
sys.path.append(os.path.join(rel_dir, '..', 'dataset-utilities'))
from common import Common  # noqa: E402


class LineCheckResult(Enum):
    OK = "OK"
    NO_COUNT = "NO (Count)"
    NO_GAPS = "NO (Gaps)"
    UNKNOWN = "Unknown"

    # make this enum JSON serializable
    def __str__(self):
        return self.value


line_checker_results_type = dict[str, LineCheckResult]


def parse_args():
    print('sys.argv: ')
    print(' '.join(sys.argv))
    print('--------------------------------------')

    parser = argparse.ArgumentParser(description="Check lines")

    # parser.add_argument("--lines", type=str, help="Path to lines file")
    # parser.add_argument("--lmdb", type=str, help="Path to lmdb")
    parser.add_argument("--input-dir", type=str, help="Path to input directory")
    parser.add_argument("--output-dir", type=str, help="Path to output directory")
    parser.add_argument("--save-images", action="store_true", help="Save rendered images")

    return parser.parse_args()


def main():
    args = parse_args()

    LineChecker(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        save_images=args.save_images
    )()

class LineChecker:
    RESULT_FILE = "line_checker_results.json"

    def __init__(self, input_dir: str, output_dir: str, save_images: bool):
        print('Running LineChecker')
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.save_images = save_images

        self.input_dir_results = os.path.join(self.input_dir, self.RESULT_FILE)

        loaded_results = {}
        if os.path.isfile(self.input_dir_results):
            loaded_results = Common.read_file(self.input_dir_results)
            loaded_results = {k: LineCheckResult(v) for k, v in loaded_results.items()}

        self.results: line_checker_results_type = loaded_results if loaded_results else {}
        self.loaded_results = loaded_results


    def __call__(self):
        os.makedirs(self.output_dir, exist_ok=True)

        files = os.listdir(self.input_dir)
        files = [file for file in files if file.endswith(".png")]
        input_files_len = len(files)

        print(f"Checking {input_files_len} images in {self.input_dir} (every dot is 200 files, every line is 2_000)")

        for i, file in enumerate(files):
            Common.print_dots(i, 200, 2_000)
            if file in self.loaded_results.keys():
                continue
            file_path = os.path.join(self.input_dir, file)
            output_path = os.path.join(self.output_dir, file.replace(".png", "_checked_lines.png"))

            result = process(file_path, output_path, self.save_images)

            self.results[file] = result
            # print(f"{file} {result}")

        # convert dictionary of [file, result] to dictionary of [result, [files]]
        result_lists = {str(result): [file for file, r in self.results.items() if r == result] for result in LineCheckResult}

        # print stats
        print('')
        print('--------------------------------------')
        print('Results:')
        print(f'From {input_files_len} input files:')
        for result, files in result_lists.items():
            print(f"\t{len(files)} are {result}")

        self.results = {k: str(v) for k, v in self.results.items()}
        Common.save_dict_as_json(self.results, self.input_dir_results)
        print(f'For results, see {self.input_dir_results}')


def detect_lines(image):
    gray = 255 - cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    width = gray.shape[1]
    min_length = int(width * 0.75)

    threshold = 50
    black_white = np.copy(gray)
    black_white[black_white < threshold] = 0
    black_white[black_white >= threshold] = 255

    lines = cv2.HoughLinesP(black_white, 1, np.pi/180, threshold=min_length, minLineLength=min_length, maxLineGap=1)

    if lines is None:
        lines = []

    lines = [line[0] for line in lines]

    return lines


def is_close_line(line1, line2, threshold=3):
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2

    # if abs(x1 - x3) < threshold and abs(y1 - y3) < threshold and abs(x2 - x4) < threshold and abs(y2 - y4) < threshold:
    if abs(y1 - y3) < threshold and abs(y2 - y4) < threshold:
        return True

    return False


def merge_close_lines(lines, threshold=3):
    clustered_lines = []

    for line in lines:
        found = False
        for cluster in clustered_lines:
            if any([is_close_line(line, cluster_line, threshold) for cluster_line in cluster]):
                cluster.append(line)
                found = True
                break

        if not found:
            clustered_lines.append([line])

    lines = []
    for cluster in clustered_lines:
        mean_x1 = int(np.mean([line[0] for line in cluster]))
        mean_y1 = int(np.mean([line[1] for line in cluster]))
        mean_x2 = int(np.mean([line[2] for line in cluster]))
        mean_y2 = int(np.mean([line[3] for line in cluster]))
        lines.append([mean_x1, mean_y1, mean_x2, mean_y2])

    return lines


def check_gaps(lines, threshold=3):
    lines = sorted(lines, key=lambda x: x[1])
    gaps = []

    for line1, line2 in zip(lines[:-1], lines[1:]):
        gap = line2[1] - line1[1]
        gaps.append(gap)

    mean_gap = np.mean(gaps)

    for gap in gaps:
        if abs(gap - mean_gap) > threshold:
            return False

    return True


def render(image, lines, color):
    for line in lines:
        cv2.line(image, (line[0], line[1]), (line[2], line[3]), color, 1, cv2.LINE_AA)


def process(input_path, output_path, save_image: bool = False) -> LineCheckResult:
    image = cv2.imread(input_path, cv2.IMREAD_COLOR)

    try:
        lines = detect_lines(image)
    # except cv2.error OpenCV(4.8.0) error assertion failed !_src.empty() in function 'cv::cvtColor'
    except cv2.error as e:
        # print(f"Error processing {input_path}: {e}")
        return LineCheckResult.UNKNOWN
    lines = merge_close_lines(lines)

    result = LineCheckResult.UNKNOWN
    color = (255, 0, 0)

    if len(lines) == 5:
        if check_gaps(lines):
            result = LineCheckResult.OK
            color = (0, 255, 0)
        else:
            result = LineCheckResult.NO_GAPS
            color = (0, 128, 255)
    else:
        result = LineCheckResult.NO_COUNT
        color = (0, 0, 255)

    if save_image:
        render(image, lines, color)
        cv2.imwrite(output_path, image)

    return result


def load(path):
    data = []

    with open(path) as file:
        for line in file:
            line = line.strip()
            if len(line) > 0:
                line_id, _ = line.split(maxsplit=1)
                data.append(line_id)
    
    return data


if __name__ == "__main__":
    main()
