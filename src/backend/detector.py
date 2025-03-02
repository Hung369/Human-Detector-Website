from typing import Tuple, Any
import cv2
from ultralytics import YOLO

class PersonDetector:
    def __init__(self, model_path: str) -> None:
        """
        Initialize the PersonDetector with a YOLO model checkpoint.
        
        :param model_path: Path to the YOLO checkpoint file.
        """
        self.model = YOLO(model_path)  # Load YOLO model from checkpoint

    def detect(self, image_path: str) -> Tuple[int, Any]:
        """
        Detect persons in an image.
        
        :param image_path: Path to the input image.
        :return: A tuple containing:
                 - the number of people detected
                 - the detection boxes from the model.
        """
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not load image from path: {image_path}")

        results = self.model(img)
        if not results:
            return 0, []
        
        boxes = results[0].boxes
        num_people = len([1 for box in boxes if int(box.cls) == 0])
        return num_people, boxes

    def visualize(self, image_path: str, boxes: Any, output_path: str) -> None:
        """
        Visualize the detection results by drawing bounding boxes on the image.
        
        :param image_path: Path to the input image.
        :param boxes: Detection boxes returned by the model.
        :param output_path: Path to save the visualized image.
        """
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not load image from path: {image_path}")

        for idx, box in enumerate(boxes):
            if int(box.cls) == 0:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

                box_height = y2 - y1
                font_scale = box_height / 100.0  

                font_scale = max(0.5, min(font_scale, 2.0))
                cv2.putText( img, f"Person {idx + 1}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, font_scale, 
                    (0, 255, 0), 2)

        cv2.imwrite(output_path, img)
