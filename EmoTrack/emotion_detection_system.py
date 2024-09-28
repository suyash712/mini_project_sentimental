import cv2
import numpy as np
from tensorflow.keras.models import model_from_json
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import get_custom_objects
import os

# Register the Sequential class to avoid deserialization issues
get_custom_objects().update({'Sequential': Sequential})

# Get the current working directory
current_dir = os.getcwd()

# Specify the paths to your model files
model_json_path = os.path.join(current_dir, 'EmoTrack', 'facialemotionmodel.json')
model_weights_path = os.path.join(current_dir, 'EmoTrack', 'facialmotionmodel.h5')

# Check if model files exist
if not os.path.exists(model_json_path):
    raise FileNotFoundError(f"Model JSON file not found at {model_json_path}")
if not os.path.exists(model_weights_path):
    raise FileNotFoundError(f"Model weights file not found at {model_weights_path}")

# Load the model architecture and weights
try:
    with open(model_json_path, 'r') as json_file:
        model_json = json_file.read()
    model = model_from_json(model_json)
    model.load_weights(model_weights_path)
except Exception as e:
    print(f"Error loading model: {str(e)}")
    exit(1)

# Define the emotion labels
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Specify the path to your video file
video_path = os.path.join(current_dir, 'EmoTrack', 'Untitled video - Made with Clipchamp.mp4')

# Check if video file exists
if not os.path.exists(video_path):
    raise FileNotFoundError(f"Video file not found at {video_path}")

# Initialize the video capture
cap = cv2.VideoCapture(video_path)

# Check if the video file was successfully opened
if not cap.isOpened():
    print(f"Error: Could not open video file at {video_path}")
    exit(1)

# Get video properties
fps = int(cap.get(cv2.CAP_PROP_FPS))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Calculate frame skip to achieve 2 FPS
frame_skip = max(1, int(fps / 2))

# Load the Haar cascade for face detection
face_cascade_path = os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml')
if not os.path.exists(face_cascade_path):
    raise FileNotFoundError(f"Haar cascade file not found at {face_cascade_path}")
face_cascade = cv2.CascadeClassifier(face_cascade_path)

# Initialize a dictionary to store detected emotions and their frame numbers
detected_emotions = {emotion: [] for emotion in emotion_labels}

frame_number = 0

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    frame_number += 1

    # Process only every frame_skip frames
    if frame_number % frame_skip != 0:
        continue

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    frame_emotions = []  # Store emotions detected in this frame

    for (x, y, w, h) in faces:
        # Extract the face ROI (Region Of Interest)
        roi_gray = gray[y:y+h, x:x+w]
        roi_gray = cv2.resize(roi_gray, (48, 48))
        roi_gray = roi_gray.astype('float') / 255.0
        roi_gray = np.expand_dims(roi_gray, axis=0)
        roi_gray = np.expand_dims(roi_gray, axis=-1)

        # Predict the emotion
        preds = model.predict(roi_gray)[0]
        emotion = emotion_labels[np.argmax(preds)]

        # Add the detected emotion to the frame_emotions list
        frame_emotions.append(emotion)

        # Store the frame number for this emotion
        detected_emotions[emotion].append(frame_number)

        # Draw the rectangle around the face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Put the emotion label text above the rectangle
        cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    # Display the resulting frame
    cv2.imshow('Face Emotion Recognition', frame)

    # Print the emotions detected in this frame
    if frame_emotions:
        print(f"Frame {frame_number}: Emotions detected - {frame_emotions}")

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()

# Print summary of emotions detected during the video
print("\nEmotion Detection Summary:")
for emotion, frames in detected_emotions.items():
    if frames:
        print(f"{emotion}: Detected in {len(frames)} frames")
        print(f"  First occurrence: Frame {min(frames)}")
        print(f"  Last occurrence: Frame {max(frames)}")
    else:
        print(f"{emotion}: Not detected")

# You can save this data to a file if needed
# with open('emotion_detection_results.txt', 'w') as f:
#     for emotion, frames in detected_emotions.items():
#         f.write(f"{emotion}: {frames}\n")