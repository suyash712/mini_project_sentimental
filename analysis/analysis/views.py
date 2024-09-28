from django.shortcuts import render,redirect, get_object_or_404 
from django.http import HttpResponse
from meeting.models import Meeting
from django.utils import timezone

def meet(request):
    return render(request,'meeting.html')

def home(request):
    return render(request,'home.html')    

def meetlist(request):
    completed_meetings = Meeting.objects.filter(is_completed=True)  # Adjust field names as necessary
    return render(request, 'list.html', {'completed_meetings': completed_meetings})

def meetoption(request):
    return render(request,'mettingoption.html')

import requests
from django.http import JsonResponse
#from zego_express_engine import ZegoExpressEngine






# views.py
from django.shortcuts import render, redirect
import jwt
import datetime





'''
from daily_co.client import DailyClient

def start_recording(request):
    daily_client = DailyClient(api_key='YOUR_DAILY_API_KEY')
    meeting_id = 'cVW0bSro3jr3xQiUqPll'  # Replace with your meeting ID

    try:
        response = daily_client.start_recording(meeting_id, layout={
            'type': 'grid',
            'participants': 'include-all'
        })
        if response['status'] == 'recording':
            return JsonResponse({'message': 'Recording started'}, status=200)
        else:
            return JsonResponse({'error': 'Failed to start recording'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def stop_recording(request):
    daily_client = DailyClient(api_key='YOUR_DAILY_API_KEY')
    meeting_id = 'cVW0bSro3jr3xQiUqPll'  # Replace with your meeting ID

    try:
        response = daily_client.stop_recording(meeting_id)
        if response['status'] == 'idle':
            # Save the recorded video to the database
            recorded_video = RecordedVideo(meeting_id=meeting_id, video_file=response['recording_urls']['mp4'])
            recorded_video.save()
            return JsonResponse({'message': 'Recording stopped and saved'}, status=200)
        else:
            return JsonResponse({'error': 'Failed to stop recording'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

        '''


from .forms import MeetingForm
from datetime import datetime
def schedule_meeting(request):
    if request.method == 'POST':
        # Get form data from POST request
        meeting_id = request.POST.get('meeting_Id')
        meeting_title = request.POST.get('meeting_title')
        meeting_date = request.POST.get('meeting_date')
        meeting_time = request.POST.get('meeting_time')

        # Combine date and time into a datetime object
        start_time_str = f"{meeting_date} {meeting_time}"
        start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M')

        # Create and save the Meeting object
        meeting = Meeting(
            meeting_id=meeting_id,
            meeting_topic=meeting_title,
            start_time=start_time,
            is_completed=False  # Set default value for now
        )
        meeting.save()

        return redirect(meeting_list)

    return render(request, 'schedule_meeting.html')
def generate_meeting_id():
    import uuid
    return str(uuid.uuid4())  # Example using UUID to generate a unique ID

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


def meetingList(request):
    meeting=Meeting.objects.all()
    return render(request,'')    


    
def join_meeting(request, meeting_id):
    meeting = Meeting.objects.get(meeting_id=meeting_id)
    return render(request, 'join_meeting.html', {'meeting': meeting})

def mark_completed_meetings():
    now = timezone.now()
    meetings = Meeting.objects.filter(is_completed=False, start_time__lt=now)
    meetings.update(is_completed=True)    


def meeting_schedule(request):
    return render(request,'meeting_schedule.html')

def meeting_success(request):
    return render(request, 'meeting_success.html')
def view_meeting_details(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    return render(request, 'meeting_details.html', {'meeting': meeting})

