import os
import argparse

from PIL import Image
from ultralytics import YOLO

from find_best_result import BestResultFinder

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", help="Model path.", type=str)
    parser.add_argument("--find-best-model-path", type=str, default='orbis_music',
                        help="If set, the best model is found automatically in given directory.")
    parser.add_argument("--images", help="Path to a directory with images.", required=True)
    parser.add_argument("--image-size", help="Image size.", required=False, default=640, type=int)
    parser.add_argument("--batch-size", help="Batch size.", required=False, default=1, type=int)
    parser.add_argument("--confidence", help="Confidence threshold.", type=float, required=False, default=0.25)
    parser.add_argument("--output-labels", help="Output label path", type=str, default='predicted_labels')

    return parser.parse_args()


def main():
    args = parse_args()

    if args.model:
        print('Loading model from args')
        model = YOLO(args.model)
    else:
        model_path = BestResultFinder(path=args.find_best_model_path)()
        if not model_path:
            raise FileNotFoundError(f'Model not found in {args.find_best_model_path}')
        print(f'Loading model: {model_path}')
        model = YOLO(model_path)

    images = [f"{os.path.join(args.images, image)}" for image in os.listdir(args.images)
              if image.endswith(".jpg") or image.endswith(".png")]

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
