import time
from ultralytics import YOLO

model = YOLO('yolo11l-seg.pt')

# Generator acts as the "video reader"
results = model.predict(source=0, show=True, stream=True)

for r in results:
    # 1/24 is approx 0.041 seconds. 
    # This forces the loop to wait before asking for the next frame.
    time.sleep(1/24)