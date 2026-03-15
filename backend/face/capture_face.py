import cv2
import os

SAVE_DIR = "backend/face/data/mohit"
os.makedirs(SAVE_DIR, exist_ok=True)

cap = cv2.VideoCapture(0)
count = 0

print("📸 Press S to capture | Q to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Capture Face", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("s"):
        path = os.path.join(SAVE_DIR, f"{count}.jpg")
        cv2.imwrite(path, frame)
        print(f"✅ Captured {path}")
        count += 1

    if key == ord("q") or count >= 20:
        break

cap.release()
cv2.destroyAllWindows()
