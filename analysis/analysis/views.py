from django.shortcuts import render,redirect, get_object_or_404 
from django.http import HttpResponse


def meet(request):
    return render(request,'meeting.html')

def home(request):
    return render(request,'home.html')    

def meetlist(request):
    return render(request,'list.html')

def meetoption(request):
    return render(request,'mettingoption.html')

import requests
from django.http import JsonResponse
#from zego_express_engine import ZegoExpressEngine
def start_recording(request):
    app_id = 'yourAppID'
    room_id = 'roomID'
    api_url = f'https://api.zegocloud.com/v1/rooms/{room_id}/start_recording'
    headers = {
        'Authorization': 'Bearer yourAPIToken',
    }
    data = {
        'appID': app_id,
        'roomID': room_id,
        'fileType': 'mp4',
        'streamType': 'audio_video'
    }

    response = requests.post(api_url, headers=headers, json=data)

    if response.status_code == 200:
        return JsonResponse({'message': 'Recording started'})
    return JsonResponse({'error': 'Failed to start recording'}, status=500)

def stop_recording(request):
    app_id = 'yourAppID'
    room_id = 'roomID'
    api_url = f'https://api.zegocloud.com/v1/rooms/{room_id}/stop_recording'
    headers = {
        'Authorization': 'Bearer yourAPIToken',
    }
    data = {
        'appID': app_id,
        'roomID': room_id
    }

    response = requests.post(api_url, headers=headers, json=data)

    if response.status_code == 200:
        return JsonResponse({'message': 'Recording stopped'})
    return JsonResponse({'error': 'Failed to stop recording'}, status=500)



