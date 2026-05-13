````md
# AI Multi Face Recognition System

## Overview

AI Multi Face Recognition System is an advanced real-time face recognition and verification application built using Python, Flask, DeepFace, ArcFace, OpenCV, RetinaFace, and MySQL.

The system can:

- Register users using webcam or uploaded images
- Generate facial embeddings using ArcFace
- Store embeddings in MySQL database
- Perform real-time face recognition
- Detect multiple faces simultaneously
- Display live face boxes and labels
- Identify unknown persons
- Show confidence scores for matched faces

This project serves as a foundation for modern AI-based security and surveillance systems.

---

# Features

## User Registration

Users can register using:

- Live webcam capture
- Image upload

The system automatically:

- Detects face
- Captures image
- Generates embeddings
- Stores embeddings in MySQL database

---

## Real-Time Face Recognition

Supports:

- Live webcam recognition
- Real-time verification
- Automatic scanning
- Multi-face recognition

---

## Multi-Face Detection

The system can detect and recognize multiple faces simultaneously.

Each detected face is:

- Compared with stored embeddings
- Assigned a confidence score
- Displayed with a live bounding box

---

## Unknown Person Detection

If a face does not match any registered embedding:

UNKNOWN

is displayed on screen.

---

## Confidence Score

Cosine similarity is used to calculate confidence percentage.

Example:

RADHEY 97%

---

## Upload Image Recognition

Users can upload images for registration and future matching.

---

# Technologies Used

## Programming Language

- Python

## Frontend

- HTML
- CSS
- JavaScript

## Backend

- Flask

## AI / Machine Learning

- DeepFace
- ArcFace
- RetinaFace
- OpenCV

## Database

- MySQL

## Additional Libraries

- NumPy
- SciPy
- Pandas
- JSON
- Base64

---

# System Architecture

```text
Webcam / Uploaded Image
            ↓
Face Detection
            ↓
Face Cropping
            ↓
ArcFace Embedding Generation
            ↓
MySQL Embedding Comparison
            ↓
Face Recognition Result
            ↓
Live Face Box + Confidence Score
````

---

# Project Structure

```text
face_verification_system/
│
├── app.py
├── live_recognition.py
├── test.py
├── requirements.txt
│
├── templates/
│   ├── index.html
│   ├── register.html
│   └── verify.html
│
├── static/
│   ├── uploads/
│   ├── css/
│   └── js/
│
└── venv/
```

---

# Database Structure

## Database Name

```sql
face_verification
```

## Users Table

```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    image_path VARCHAR(255),
    embedding LONGTEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

# Installation Guide

## Step 1 — Clone Repository

```bash
git clone https://github.com/your-username/AI-Multi-Face-Recognition-System.git
```

---

## Step 2 — Create Virtual Environment

```bash
python -m venv venv
```

---

## Step 3 — Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

---

## Step 4 — Install Dependencies

```bash
pip install flask
pip install deepface
pip install tensorflow
pip install mysql-connector-python
pip install opencv-python
pip install retina-face
pip install scipy
pip install numpy
pip install pandas
```

---

# Running the Project

## Run Flask Application

```bash
python app.py
```

---

## Run Real-Time Recognition System

```bash
python live_recognition.py
```

---

# Routes

| Route     | Description       |
| --------- | ----------------- |
| /         | Home Page         |
| /register | Register New User |
| /verify   | Live Verification |

---

# Working Principle

## Step 1 — Face Registration

The user registers using webcam or uploaded image.

The system:

* Captures face
* Saves image
* Generates embeddings
* Stores embeddings in MySQL

---

## Step 2 — Real-Time Recognition

The webcam continuously scans faces.

Detected faces are:

* Cropped
* Converted into embeddings
* Compared with database embeddings

---

## Step 3 — Matching

Cosine similarity is used to compare embeddings.

If similarity score is below threshold:

MATCH FOUND

Otherwise:

UNKNOWN

is displayed.

---

# Performance Optimizations

Several optimizations were implemented:

* Frame skipping
* Lower camera resolution
* Cached recognition
* Faster Haar Cascade detection
* Delayed recognition intervals

These optimizations improve:

* FPS
* CPU usage
* Real-time smoothness

---

# Current Limitations

* CPU-based inference may cause lag
* No anti-spoofing yet
* No GPU acceleration yet
* Lighting affects recognition accuracy
* Glasses and side-angle variations may reduce confidence

---

# Future Improvements

## Planned Features

* Anti-spoofing system
* Blink detection
* Head movement verification
* Attendance management system
* Admin dashboard
* Face search in group photos
* Unknown person alerts
* GPU acceleration
* AI surveillance integration
* Mobile camera support
* Cloud deployment

---

# Applications

This project can be used in:

* Smart attendance systems
* AI-based hostel entry systems
* Office security systems
* Surveillance systems
* Classroom automation
* Face authentication systems
* Smart access control systems

---

# Learning Outcomes

This project demonstrates practical implementation of:

* Artificial Intelligence
* Machine Learning
* Computer Vision
* Face Recognition
* Real-Time Video Processing
* Database Integration
* Flask Web Development

---

# Conclusion

The AI Multi Face Recognition System is a powerful real-time AI application capable of detecting and recognizing multiple faces using modern deep learning models.

The project combines:

* Deep Learning
* Computer Vision
* Database Systems
* Real-Time Processing
* Web Technologies

into a complete intelligent face recognition platform.

This system serves as a strong foundation for advanced AI security and surveillance applications.

```

