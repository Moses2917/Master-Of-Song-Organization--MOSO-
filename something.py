from ultralytics import YOLO
import cv2

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

model = YOLO('yolov8x-seg.pt')
cap, frame = vc.read()
while True:
    cap, frame = vc.read()
    vci = cv2.resize(frame, (150, 300))
    results = model(frame, boxes=True,show=True)