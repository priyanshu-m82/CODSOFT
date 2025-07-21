import cv2
import face_recognition
import os

# Directory with known faces
known_dir = 'known_faces'
known_encodings = []
known_names = []

# Load known faces
for filename in os.listdir(known_dir):
    if filename.endswith(('.jpg', '.png')):
        image = face_recognition.load_image_file(os.path.join(known_dir, filename))
        encoding = face_recognition.face_encodings(image)
        if encoding:
            known_encodings.append(encoding[0])
            known_names.append(os.path.splitext(filename)[0])
        else:
            print(f"Could not encode {filename}")

print("Loaded known faces:", known_names)

# Start webcam
cap = cv2.VideoCapture(0)
print("Webcam started. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Detect faces
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            best_match_index = matches.index(True)
            name = known_names[best_match_index]

        # Scale back face locations to original frame size
        top, right, bottom, left = [v * 4 for v in face_location]
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Show video window
    cv2.imshow('Face Recognition', frame)

    # Press 'q' to quit
    key = cv2.waitKey(1)
    if key == ord('q') or key == 27:  # 'q' or ESC to quit
        print("Quitting...")
        break

cap.release()
cv2.destroyAllWindows()