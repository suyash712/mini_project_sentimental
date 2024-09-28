from django import forms
from meeting.models import Meeting

class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['meeting_topic', 'start_time']