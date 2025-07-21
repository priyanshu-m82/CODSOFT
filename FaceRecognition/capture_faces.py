import cv2
import os

# Ensure the directory exists
known_dir = "known_faces"
os.makedirs(known_dir, exist_ok=True)

# Ask for the user's name
name = input("Enter your name: ").strip()
filename = f"{name}.jpg"
filepath = os.path.join(known_dir, filename)

# Start webcam
cap = cv2.VideoCapture(0)
print("Press 's' to capture your face. Press 'q' to quit without saving.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    cv2.imshow("Capture Face", frame)

    key = cv2.waitKey(1)
    if key == ord('s'):
        cv2.imwrite(filepath, frame)
        print(f"Saved to {filepath}")
        break
    elif key == ord('q'):
        print("Quit without saving.")
        break

cap.release()
cv2.destroyAllWindows()