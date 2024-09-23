import cv2
import numpy as np
import tensorflow as tf
import os
import sqlite3
from datetime import datetime


os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
print(os.environ)

# Load the model
json_file = open("emotiondetector.json", "r")
model_json = json_file.read()
json_file.close()

# Use TensorFlow's built-in functions to load the model
model = tf.keras.models.model_from_json(model_json)
model.load_weights("facialmotionmodel.h5")

# Define emotions
emotions = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

# Function to preprocess the image
def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    if len(faces) > 0:
        (x, y, w, h) = faces[0]
        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (48, 48))
        face = np.expand_dims(face, axis=0)
        face = np.expand_dims(face, axis=-1)
        face = face / 255.0
        return face
    return None

# Function to predict emotion
def predict_emotion(face):
    prediction = model.predict(face)
    return emotions[np.argmax(prediction)]

# Function to save image and emotion to database
def save_to_database(image_path, emotion, timestamp):
    conn = sqlite3.connect('interview_emotions.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS emotions
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       image_path TEXT,
                       emotion TEXT,
                       timestamp TEXT)''')
    cursor.execute("INSERT INTO emotions (image_path, emotion, timestamp) VALUES (?, ?, ?)",
                   (image_path, emotion, timestamp))
    conn.commit()
    conn.close()

# Function to process recorded video
def process_recorded_video(video_path, interval=1):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_count % (interval * int(cap.get(cv2.CAP_PROP_FPS))) == 0:
            face = preprocess_image(frame)
            if face is not None:
                emotion = predict_emotion(face)
                timestamp = datetime.fromtimestamp(cap.get(cv2.CAP_PROP_POS_MSEC)/1000.0).strftime("%Y%m%d_%H%M%S")
                image_path = f"interview_frames/frame_{timestamp}.jpg"
                os.makedirs("interview_frames", exist_ok=True)
                cv2.imwrite(image_path, frame)
                save_to_database(image_path, emotion, timestamp)
                print(f"Processed frame at {timestamp}: Emotion - {emotion}")
        
        frame_count += 1
    
    cap.release()

# Main function to process the recorded interview
def analyze_recorded_interview(video_path, interval=1):
    process_recorded_video(video_path, interval)

# Run the emotion analysis system
if __name__ == "__main__":
    video_path = "C:/Users/sandh/Downloads/test.mp4"  # Replace with the path to your recorded video
    analyze_recorded_interview(video_path, interval=1)  # Process every second of the video