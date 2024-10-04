from django.db import models

# Create your models here.


class Meeting(models.Model):
    meeting_id = models.CharField(max_length=200)
    meeting_topic = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    file = models.FileField(upload_to='uploads/', null=True, blank=True, default=None)

    def __str__(self):
        return self.meeting_topic


class EmotionData(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)  # Assuming you have a Meeting model
    timestamp = models.FloatField()  # Time of the emotion capture
    emotion = models.CharField(max_length=100)  # Emotion type (e.g., "Confidence", "Nervousness")
    intensity = models.FloatField()
    # Emotion intensity (0.0 to 1.0)

    def __str__(self):
        return f"{self.emotion} at {self.timestamp}"
    
    