from django.contrib import admin
from .models import Meeting,EmotionData

# Register your models here.
class Meeting(admin.ModelAdmin):
    list_display=(
        'meeting_id','meeting_topic','start_time','is_completed'
    )
    admin.site.register(Meeting)


class EmotionData(admin.ModelAdmin):
    list_display=(
        'meeting','timestamp','emotion','intensity'
    )    
    admin.site.register(EmotionData)