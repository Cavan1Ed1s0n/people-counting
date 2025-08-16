import os
import io
import uuid

import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO


model = YOLO('yolov8n.pt')  # Pre-trained YOLOv8 nano model

def detect_people(image_bytes: bytes) -> tuple[int, str]:
    # Load image
    image = Image.open(io.BytesIO(image_bytes))
    results = model(image)  # Run detection

    # Count people (class 0 in COCO is 'person')
    num_people = 0
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    for result in results:
        for box in result.boxes:
            if int(box.cls) == 0:  # Person class
                num_people += 1
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(img_cv, (x1, y1), (x2, y2), (0, 255, 0), 2)



    return img_cv, num_people

