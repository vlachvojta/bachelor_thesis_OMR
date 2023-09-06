import argparse

from safe_gpu.safe_gpu import GPUOwner

from ultralytics import YOLO


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", help="Model path.", required=True)
    parser.add_argument("--dataset", help="Path to the dataset YAML file.", required=True)
    parser.add_argument("--epochs", help="Number of training epochs.", required=False, default=100, type=int)
    parser.add_argument("--patience", help="Number of patience epochs.", required=False, default=50, type=int)
    parser.add_argument("--batch-size", help="Batch size.", required=False, default=16, type=int)
    parser.add_argument("--image-size", help="Image size.", required=False, default=640, type=int)
    parser.add_argument("--save-step", help="Number of epochs after which the checkpoint is saved.", required=False, default=1, type=int)
    parser.add_argument("--use-pretrained", help="If set, pretrained model is used.", action="store_true")
    parser.add_argument("--optimizer", help="Optimizer used for training.", required=False, default="Adam", choices=["SGD", "Adam", "Adamax", "AdamW", "NAdam", "RAdam", "RMSProp", "auto"])
    parser.add_argument("--learning-rate", help="Learning rate.", required=False, default=0.00020, type=float)
    parser.add_argument("--close-mosaic", help="Number of final epochs during which mosaic is disabled.", required=False, default=10, type=int)
    parser.add_argument("--project", help="Name of the project.", required=False, default="orbis_music")
    parser.add_argument("--name", help="Name of the experiment.", required=False, default="staff_detector")
    parser.add_argument("--workers", help="Number of workers.", required=False, default=8, type=int)

    return parser.parse_args()


def main():
    args = parse_args()

    gpu_owner = GPUOwner()

    model = YOLO(args.model)
    model.train(data=args.dataset,
                epochs=args.epochs,
                patience=args.patience,
                batch=args.batch_size,
                imgsz=args.image_size,
                val=True,
                save=True,
                save_period=args.save_step,
                pretrained=args.use_pretrained,
                optimizer=args.optimizer,
                lr0=args.learning_rate,
                close_mosaic=args.close_mosaic,
                project=args.project,
                name=args.name,
                workers=args.workers,
                device=0)

    return 0


if __name__ == "__main__":
    exit(main())
