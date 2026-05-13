from flask import Flask, render_template, request, jsonify
from deepface import DeepFace
import mysql.connector
import os
import base64
import json
import numpy as np
from scipy.spatial.distance import cosine

app = Flask(__name__)

# -----------------------------
# PATH SETUP
# -----------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

print("UPLOAD FOLDER:", UPLOAD_FOLDER)

# -----------------------------
# MYSQL CONNECTION
# -----------------------------

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="core#85208520",
    database="face_verification"
)

cursor = db.cursor()

print("MYSQL CONNECTED")

# -----------------------------
# ROUTES
# -----------------------------

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/verify')
def verify():
    return render_template("verify.html")


# -----------------------------
# SAVE FACE
# -----------------------------

@app.route('/save_face', methods=['POST'])
def save_face():

    try:

        data = request.get_json()

        image_data = data['image']
        name = data['name']

        print("NAME:", name)

        # Remove base64 header
        image_data = image_data.split(",")[1]

        # Decode image
        image_bytes = base64.b64decode(image_data)

        # Create filename
        filename = f"{name}.png"

        filepath = os.path.join(UPLOAD_FOLDER, filename)

        print("FILE PATH:", filepath)

        # Save image
        with open(filepath, "wb") as f:
            f.write(image_bytes)

        print("IMAGE SAVED")

        # -----------------------------
        # DEEPFACE EMBEDDING
        # -----------------------------

        embedding = DeepFace.represent(
            img_path=filepath,
            model_name='ArcFace',
            detector_backend='retinaface',
            enforce_detection=True
        )

        face_embedding = embedding[0]['embedding']

        print("EMBEDDING GENERATED")

        # Convert embedding to JSON
        embedding_json = json.dumps(face_embedding)

        # -----------------------------
        # SAVE TO MYSQL
        # -----------------------------

        sql = """
        INSERT INTO users (name, image_path, embedding)
        VALUES (%s, %s, %s)
        """

        values = (name, filepath, embedding_json)

        cursor.execute(sql, values)

        db.commit()

        print("DATA SAVED TO MYSQL")

        return jsonify({
            "message": f"{name} Registered Successfully"
        })

    except Exception as e:

        print("ERROR:", str(e))

        return jsonify({
            "message": str(e)
        }), 500

# -----------------------------
# VERIFY FACE
# -----------------------------

@app.route('/verify_face', methods=['POST'])
def verify_face():

    try:

        data = request.get_json()

        image_data = data['image']

        # Remove base64 header
        image_data = image_data.split(",")[1]

        image_bytes = base64.b64decode(image_data)

        temp_path = os.path.join(UPLOAD_FOLDER, "temp_verify.png")

        # Save temporary image
        with open(temp_path, "wb") as f:
            f.write(image_bytes)

        print("TEMP IMAGE SAVED")

        # Generate embedding
        embedding = DeepFace.represent(
            img_path=temp_path,
            model_name='ArcFace',
            enforce_detection=True
        )

        current_embedding = embedding[0]['embedding']

        print("CURRENT EMBEDDING GENERATED")

        # Fetch all users
        cursor.execute("SELECT name, embedding FROM users")

        users = cursor.fetchall()

        best_match = None

        best_score = 999

        # Compare embeddings
        for user in users:

            db_name = user[0]

            db_embedding = json.loads(user[1])

            similarity = cosine(
                current_embedding,
                db_embedding
            )

            print(db_name, similarity)

            if similarity < best_score:

                best_score = similarity

                best_match = db_name

        # Threshold
        if best_score < 0.50:

            confidence = round((1 - best_score) * 100, 2)

            return jsonify({
                "message":
                f"MATCH FOUND: {best_match} | Confidence: {confidence}%"
            })

        else:

            return jsonify({
                "message":
                "NO MATCH FOUND"
            })

    except Exception as e:

        print("VERIFY ERROR:", str(e))

        return jsonify({
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)