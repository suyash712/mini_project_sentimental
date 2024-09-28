from django.contrib import admin
from .models import Meeting

# Register your models here.
class Meeting(admin.ModelAdmin):
    list_display=(
        'meeting_id','meeting_topic','start_time','is_completed'
    )
    admin.site.register(Meeting)