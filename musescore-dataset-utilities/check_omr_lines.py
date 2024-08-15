import os
import cv2
import lmdb
import argparse
import numpy as np



def parse_args():
    parser = argparse.ArgumentParser(description="Check lines")

    parser.add_argument("--lines", type=str, help="Path to lines file")
    parser.add_argument("--lmdb", type=str, help="Path to lmdb")

    return parser.parse_args()


def detect_lines(image):
    gray = 255 - cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    width = gray.shape[1]
    min_length = int(width * 0.75)

    threshold = 80
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


def load_image(txn, image_name):
    return cv2.imdecode(np.frombuffer(txn.get(image_name.encode()), dtype=np.uint8), 1)


def process(line, txn):
    # image = cv2.imread(input_path, cv2.IMREAD_COLOR)

    image = load_image(txn, line)
    
    lines = detect_lines(image)
    lines = merge_close_lines(lines)

    result = "Unknown"
    color = (255, 0, 0)

    if len(lines) == 5:
        if check_gaps(lines):
            result = "OK"
            color = (0, 255, 0)
        else:
            result = "NO (Gaps)"
            color = (0, 128, 255)
    else:
        result = "NO (Count)"
        color = (0, 0, 255)

    # render(image, lines, color)
    # cv2.imwrite(output_path, image)

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


def main():
    args = parse_args()

    lines = load(args.lines)
    
    env = lmdb.open(args.lmdb, readonly=True, lock=False)
    with env.begin() as txn:
        for line in lines:
            result = process(line, txn)

            # if result.startswith("NOT"):
            #     result = "NOT"

            print(f"{line} {result}")

    return 0


if __name__ == "__main__":
    exit(main())
