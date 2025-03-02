import argparse
from collections import defaultdict
import cv2
import numpy as np
from ultralytics import YOLO

def track_video(input_video_path, output_video_path):
    model = YOLO("yolo11n.pt")

    cap = cv2.VideoCapture(input_video_path)
    track_history = defaultdict(list)

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (frame_width, frame_height))

    while cap.isOpened():
        success, frame = cap.read()
        if success:
            results = model.track(frame, persist=True, tracker="botsort.yaml")
            if hasattr(results[0].boxes, 'id') and results[0].boxes.id is not None:
                boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
                ids = results[0].boxes.id.cpu().numpy().astype(int)

                # Draw boxes and IDs on the frame
                for box, id in zip(boxes, ids):
                    cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 1)
                    cv2.putText(frame, f"Id {id}", (box[0], box[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)

            cv2.imshow('Video Feed', frame)
            out.write(frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    return output_video_path

def parse_args():
    parser = argparse.ArgumentParser(
        description="Track objects in a video using YOLO with a specified tracker."
    )
    parser.add_argument(
        "--input", type=str, required=True,
        help="Path to the input video file"
    )
    parser.add_argument(
        "--output", type=str, required=True,
        help="Path to save the output tracked video"
    )
    parser.add_argument(
        "--weights", type=str, required=True,
        help="Path to the model weights file"
    )
    parser.add_argument(
        "--tracker", type=str, required=True,
        help="Path to the tracker configuration file (e.g., botsort.yaml)"
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    processed_video_path = track_video(args.input, args.output, args.weights, args.tracker)
    print(f"Processed video saved to: {processed_video_path}")