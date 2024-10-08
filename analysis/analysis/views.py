from django.shortcuts import render,redirect, get_object_or_404 
from django.http import HttpResponse
from meeting.models import Meeting,EmotionData
from django.utils import timezone
from .ml_model.emotion_detection_system import analyze_video
import datetime
import requests
from django.http import JsonResponse
from .forms import MeetingForm
from datetime import datetime

from django.shortcuts import render, redirect
import jwt
import datetime
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage

def meet(request):
    return render(request,'meeting.html')

def home(request):
    return render(request,'home.html')    

def meetlist(request):
    completed_meetings = Meeting.objects.filter(is_completed=True)  # Adjust field names as necessary
    return render(request, 'list.html', {'completed_meetings': completed_meetings})

def meetoption(request):
    return render(request,'mettingoption.html')

def meeting_schedule(request):
    return render(request,'meeting_schedule.html')

#from zego_express_engine import ZegoExpressEngine


def schedule_meeting(request):
    if request.method == 'POST':
        # Get form data from POST request
        meeting_id = request.POST.get('meeting_id')  # Fixed the key from 'meeting_Id' to 'meeting_id'
        meeting_title = request.POST.get('meeting_title')
        meeting_date = request.POST.get('meeting_date')
        meeting_time = request.POST.get('meeting_time')

        # Combine date and time into a datetime object
        try:
            start_time_str = f"{meeting_date} {meeting_time}"
            start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M')
        except ValueError:
            return HttpResponse("Invalid date or time format", status=400)

        # Create and save the Meeting object
        meeting = Meeting(
            meeting_id=meeting_id,
            meeting_topic=meeting_title,
            start_time=start_time,
            is_completed=False  # Set default value for now
        )
        
        try:
            meeting.save()
        except Exception as e:
            return HttpResponse(f"An error occurred while saving the meeting: {str(e)}", status=500)

        return redirect('meeting_list')  # Ensure 'meeting_list' is a valid URL name

    return render(request, 'schedule_meeting.html')
 # Example using UUID to generate a unique ID

def meeting_list(request):
    # Get the current time
    current_time = timezone.now()

    # Automatically mark meetings as completed if their start time has passed
    Meeting.objects.filter(start_time__lt=current_time, is_completed=False).update(is_completed=True)

    # Filter upcoming and previous meetings based on the 'is_completed' field
    upcoming_meetings = Meeting.objects.filter(is_completed=False).order_by('start_time')
    previous_meetings = Meeting.objects.filter(is_completed=True).order_by('-start_time')

    # Pass the meetings to the template
    context = {
        'upcoming_meetings': upcoming_meetings,
        'previous_meetings': previous_meetings
    }
    return render(request, 'mettingoption.html', context)

 


    
def join_meeting(request, meeting_id):
    meeting = Meeting.objects.get(meeting_id=meeting_id)
    return render(request, 'join_meeting.html', {'meeting': meeting})

  
def meeting_success(request):
    return render(request, 'meeting_success.html')

def view_meeting_details(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    return render(request, 'meeting_details.html', {'meeting': meeting})

def login(request):
    return render(request,'login.html')



# Handle file/video upload


def upload_meeting_file(request, meeting_id):
    meetings = Meeting.objects.filter(meeting_id=meeting_id)
    if not meetings.exists():
        return HttpResponse('Meeting not found')

    if request.method == 'POST' and request.FILES.get('meeting_file'):
        meeting_file = request.FILES['meeting_file']
        
        # Update the file for all meetings with this meeting_id
        for meeting in meetings:
            meeting.file = meeting_file
            meeting.save()

        return redirect(meeting_list)
# Handle marking the meeting as completed

  # Redirect to the relevant page after marking as completed
  # redirect to the meeting page or another page

    



import os
import cv2
from django.utils import timezone

from .ml_model.emotion_detection_system import analyze_video  # Import your ML model function

def process_meeting_video(meeting_id):
    try:
        # Get the meeting from the database
        meeting = Meeting.objects.get(meeting_id=meeting_id)

        # Ensure the meeting has a video file associated
        if not meeting.file:
            raise FileNotFoundError(f"No video file found for meeting {meeting_id}")

        # Path to the video file
        video_path = meeting.file.path  # Full file path in Django

        # Analyze the video using your ML model
        detected_emotions = analyze_video(video_path)

        # Save detected emotions to the database
        for emotion, frames in detected_emotions.items():
            for frame in frames:
                # Create an EmotionData object for each detected emotion
                EmotionData.objects.create(
                    meeting=meeting,
                    timestamp=timezone.now(),  # Use current time or frame-based timestamp
                    emotion=emotion,
                    intensity=1.0  # Assume intensity is 1.0, you can adjust this based on your model
                )

        print(f"Emotion data saved for meeting {meeting_id}")

    except Meeting.DoesNotExist:
        print(f"Meeting with ID {meeting_id} does not exist.")
    except Exception as e:
        print(f"Error processing video for meeting {meeting_id}: {str(e)}")

from django.http import JsonResponse
# Assuming you have models for Meeting and EmotionData
from django.shortcuts import get_object_or_404
import datetime

def perform_emotion_analysis(video_file):
    """
    Placeholder function for performing emotion analysis on a video file.
    This should include your emotion detection logic, which processes the video,
    analyzes emotions, and returns the results.
    """
    # Your emotion analysis logic goes here.
    # This function should return True/False or a detailed result after analysis.
    try:
        # Perform the emotion analysis on the video file
        # Analyze the file using a machine learning model or other analysis tool
        # For now, let's assume the analysis is successful.
        # Replace this with actual logic to analyze the video.
        analyzed_emotions = {
            "happy": 0.5,
            "sad": 0.2,
            "angry": 0.3
        }
        return analyzed_emotions
    except Exception as e:
        print(f"Error during emotion analysis: {e}")
        return None
    
def meeting_detail(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk)
    return render(request, 'meeting_detail.html', {'meeting': meeting})    

from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse

import cv2
import numpy as np
from tensorflow.keras.models import model_from_json
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Define the emotion labels
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Load the emotion detection model
def load_emotion_model():
    current_dir = os.getcwd()
    model_json_path = os.path.join(current_dir, 'analysis', 'facialemotionmodel.json')
    model_weights_path = os.path.join(current_dir, 'analysis', 'facialmotionmodel.h5')

    with open(model_json_path, 'r') as json_file:
        model_json = json_file.read()
    model = model_from_json(model_json)
    model.load_weights(model_weights_path)
    return model

model = load_emotion_model()
from django.core.cache import cache

def analyze_meeting_emotions(meeting_id):
    print(f"Analyzing meeting with ID: {meeting_id}")
    meeting = get_object_or_404(Meeting, meeting_id=meeting_id)

    if not meeting.file:
        return {'error': 'No video file uploaded for this meeting'}

    video_path = meeting.file.path  # Get the path to the uploaded video

    # Load the Haar cascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Initialize video capture
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return {'error': 'Could not open video file'}

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_skip = max(1, int(fps / 2))  # Process 2 FPS

    detected_emotions = {emotion: [] for emotion in emotion_labels}
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

            preds = model.predict(roi_gray)[0]
            emotion = emotion_labels[np.argmax(preds)]
            detected_emotions[emotion].append(frame_number)

            # Calculate video time (in seconds)
            video_time = frame_number / fps  # This should be a float representing seconds

            # Save the emotion to the database with video time
            EmotionData.objects.create(
                meeting=meeting,
                timestamp=video_time,  # This should be a float (seconds from start of video)
                emotion=emotion,
                intensity=float(np.max(preds))
            )

    cap.release()
    return detected_emotions



from django.core.cache import cache
def analyze_meeting_view(request, meeting_id):
    meeting = get_object_or_404(Meeting, meeting_id=meeting_id)
    if request.method == 'POST':
        try:
            emotions_summary = analyze_meeting_emotions(meeting_id)
            if 'error' in emotions_summary:
                return JsonResponse({'success': False, 'error': emotions_summary['error']}, status=400)
            
            meeting.is_completed = True
            meeting.save()
            return redirect(meeting_list)
        except Exception as e:
            logger.error(f"Error analyzing meeting {meeting_id}: {str(e)}")
            return JsonResponse({'success': False, 'error': 'An unexpected error occurred. Please try again.'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def get_analysis_progress(request, meeting_id):
    if request.method == 'GET':
        progress = cache.get(f'analysis_progress_{meeting_id}', 0)  # Default progress is 0 if not found
        return JsonResponse({'progress': progress})
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def get_emotion_data(request, meeting_id):
    meeting = get_object_or_404(Meeting, meeting_id=meeting_id)
    emotions = EmotionData.objects.filter(meeting=meeting).order_by('timestamp')  # Get emotions for the meeting
    emotion_data = {
        'emotions': [
            {
                'timestamp': emotion.timestamp,
                'emotion': emotion.emotion,
                'intensity': emotion.intensity,
            }
            for emotion in emotions
        ]
    }
    return JsonResponse(emotion_data)  

    