from django.db import models

# Create your models here.
class Meeting(models.Model):
    meeting_id = models.CharField(max_length=200)
    meeting_topic = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.meeting_topic
    
    