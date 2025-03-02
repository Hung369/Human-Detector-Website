#Training YOLOv11 for Human Tracking

from ultralytics import YOLO


if __name__ == '__main__':
    model = YOLO('yolo11n.pt')
    results = model.train(data="./datasets/data.yaml", epochs=300, imgsz=640, device=0, save=True)