import cv2
import numpy as np
from tensorflow.keras.models import model_from_json
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import get_custom_objects
import os

# Register the Sequential class to avoid deserialization issues
get_custom_objects().update({'Sequential': Sequential})

def analyze_video(video_path):
    # Get the current working directory
    current_dir = os.getcwd()

    # Specify the paths to your model files
    model_json_path = os.path.join(current_dir, 'EmoTrack', 'facialemotionmodel.json')
    model_weights_path = os.path.join(current_dir, 'EmoTrack', 'facialmotionmodel.h5')

    # Load the model architecture and weights
    with open(model_json_path, 'r') as json_file:
        model_json = json_file.read()
    model = model_from_json(model_json)
    model.load_weights(model_weights_path)

    # Define the emotion labels
    emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

    # Initialize the video capture
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file at {video_path}")
        return []

    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_skip = max(1, int(fps / 2))  # Skip frames to process at 2 FPS

    # Load the Haar cascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    detected_emotions = []

    frame_number = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_number += 1

        if frame_number % frame_skip != 0:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_gray = cv2.resize(roi_gray, (48, 48))
            roi_gray = roi_gray.astype('float') / 255.0
            roi_gray = np.expand_dims(roi_gray, axis=0)
            roi_gray = np.expand_dims(roi_gray, axis=-1)

            # Predict the emotion
            preds = model.predict(roi_gray)[0]
            emotion = emotion_labels[np.argmax(preds)]
            intensity = np.max(preds)  # Max probability as intensity

            # Append the emotion data to the list
            detected_emotions.append({
                'timestamp': frame_number / fps,  # Convert frame number to seconds
                'emotion': emotion,
                'intensity': intensity
            })

    cap.release()

    return detected_emotions  # Return a list of emotion data dictionaries
