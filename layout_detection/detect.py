import os
import argparse

from PIL import Image
from ultralytics import YOLO


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", help="Model path.", required=True)
    parser.add_argument("--images", help="Path to a directory with images.", required=True)
    parser.add_argument("--image-size", help="Image size.", required=False, default=640, type=int)
    parser.add_argument("--batch-size", help="Batch size.", required=False, default=1, type=int)
    parser.add_argument("--confidence", help="Confidence threshold.", type=float, required=False, default=0.25)
    parser.add_argument("--output-labels", help="Output label path", type=str, default='predicted_labels')

    return parser.parse_args()


def main():
    args = parse_args()

    images = [f"{os.path.join(args.images, image)}" for image in os.listdir(args.images)
              if image.endswith(".jpg") or image.endswith(".png")]
    model = YOLO(args.model)

    for image in images:
        result = model.predict(
            source=image,
            imgsz=args.image_size,
            conf=args.confidence,
            save_txt=True,
            device=0)[0]

        # Show the results
        im_array = result.plot()  # plot a BGR numpy array of predictions
        im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image

        # Save the results to image
        if not os.path.exists(os.path.join(result.save_dir, 'images')):
            os.makedirs(os.path.join(result.save_dir, 'images'))
        im.save(os.path.join(result.save_dir, 'images', os.path.basename(image)))  # save image

    return 0


if __name__ == "__main__":
    main()
