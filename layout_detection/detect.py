import os
import argparse

from safe_gpu.safe_gpu import GPUOwner

from ultralytics import YOLO


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", help="Model path.", required=True)
    parser.add_argument("--images", help="Path to a directory with images.", required=True)
    parser.add_argument("--image-size", help="Image size.", required=False, default=640, type=int)
    parser.add_argument("--batch-size", help="Batch size.", required=False, default=1, type=int)
    parser.add_argument("--confidence", help="Confidence threshold.", required=True, type=float)
    parser.add_argument("--labels", help="Path to a directory with predicted labels.", required=True)

    return parser.parse_args()


def main():
    args = parse_args()

    gpu_owner = GPUOwner()

    images = [f"{os.path.join(args.images, image)}" for image in os.listdir(args.images) if image.endswith(".jpg") or image.endswith(".png")]
    model = YOLO(args.model)

    while images:
        batch = images[:args.batch_size]
        images = images[args.batch_size:]

        result = model(batch, 
                       imgsz=args.image_size,
                       conf=args.confidence,
                       save_txt=True,
                       device=0)

    return 0


if __name__ == "__main__":
    exit(main())
