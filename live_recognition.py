from deepface import DeepFace
from scipy.spatial.distance import cosine
import mysql.connector
import cv2
import json
import time

# -----------------------------
# MYSQL CONNECTION
# -----------------------------

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="core#85208520",
    database="face_verification"
)

cursor = db.cursor(buffered=True)

print("MYSQL CONNECTED")

# -----------------------------
# LOAD USERS
# -----------------------------

cursor.execute("SELECT name, embedding FROM users")

users = cursor.fetchall()

print("USERS LOADED:", len(users))

# -----------------------------
# FACE DETECTOR
# -----------------------------

face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    'haarcascade_frontalface_default.xml'
)

# -----------------------------
# CAMERA
# -----------------------------

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# -----------------------------
# PERFORMANCE VARIABLES
# -----------------------------

last_recognition_time = 0

cached_faces = []

recognition_interval = 2  # seconds

# -----------------------------
# MAIN LOOP
# -----------------------------

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1)

    frame = cv2.resize(frame, (640, 480))

    current_time = time.time()

    # -----------------------------
    # ONLY RECOGNIZE EVERY X SECONDS
    # -----------------------------

    if current_time - last_recognition_time > recognition_interval:

        cached_faces = []

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_detector.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(80, 80)
        )

        for (x, y, w, h) in faces:

            x1 = x
            y1 = y
            x2 = x + w
            y2 = y + h

            face = frame[y1:y2, x1:x2]

            try:

                embedding = DeepFace.represent(
                    img_path=face,
                    model_name='ArcFace',
                    detector_backend='skip',
                    enforce_detection=False
                )

                current_embedding = embedding[0]['embedding']

                best_match = "UNKNOWN"

                best_score = 999

                # -----------------------------
                # DATABASE COMPARISON
                # -----------------------------

                for user in users:

                    db_name = user[0]

                    db_embedding = json.loads(user[1])

                    similarity = cosine(
                        current_embedding,
                        db_embedding
                    )

                    if similarity < best_score:

                        best_score = similarity

                        best_match = db_name

                # -----------------------------
                # MATCH LOGIC
                # -----------------------------

                if best_score < 0.68:

                    confidence = round(
                        (1 - best_score) * 100,
                        2
                    )

                    label = f"{best_match} {confidence}%"

                    color = (0, 255, 0)

                else:

                    label = "UNKNOWN"

                    color = (0, 0, 255)

                cached_faces.append({
                    "x1": x1,
                    "y1": y1,
                    "x2": x2,
                    "y2": y2,
                    "label": label,
                    "color": color
                })

            except Exception as e:

                print("FACE ERROR:", str(e))

        last_recognition_time = current_time

    # -----------------------------
    # DRAW CACHED BOXES
    # -----------------------------

    for face_data in cached_faces:

        x1 = face_data["x1"]
        y1 = face_data["y1"]
        x2 = face_data["x2"]
        y2 = face_data["y2"]

        label = face_data["label"]

        color = face_data["color"]

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            color,
            2
        )

        cv2.rectangle(
            frame,
            (x1, y1 - 35),
            (x2, y1),
            color,
            -1
        )

        cv2.putText(
            frame,
            label,
            (x1 + 5, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

    # -----------------------------
    # SHOW WINDOW
    # -----------------------------

    cv2.imshow(
        "AI Multi Face Recognition",
        frame
    )

    # -----------------------------
    # EXIT
    # -----------------------------

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# -----------------------------
# CLEANUP
# -----------------------------

cap.release()

cv2.destroyAllWindows()