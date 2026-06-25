import cv2
from ultralytics import YOLO
import os

# 1. Load your best weights
model = YOLO(r"C:\Users\Misbah\Downloads\Teknofest\best.pt")

# 2. Path to your image
img_path = r"C:\Users\Misbah\Downloads\a--106-_jpg.rf.91d96709e138f736cfa146e73fb24279.jpg"

# 3. Run Inference
# We set conf=0.25 to remove the "Box Soup" 
# We set imgsz=640 to match your Kaggle training resolution
results = model.predict(source=img_path, conf=0.25, imgsz=640)

# 4. Save and Show the "Clean" Result
res = results[0]
if len(res.boxes) > 0:
    print(f"✅ Found {len(res.boxes)} UAV(s) with high confidence!")
    for box in res.boxes:
        print(f"Confidence: {box.conf[0].item():.2f}")
else:
    print("❌ No detections found at 0.25 confidence. The model is not confident enough.")

# Plot the result with professional settings
annotated_img = res.plot(line_width=2, labels=True, boxes=True)

# Save the clean version for your Teknofest CDR report
output_save_path = r"C:\Users\Misbah\Downloads\Teknofest\Clean_Detection_Result.jpg"
cv2.imwrite(output_save_path, annotated_img)

cv2.imshow("Teknofest - Professional View", annotated_img)
cv2.waitKey(0)
cv2.destroyAllWindows()