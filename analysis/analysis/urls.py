"""
URL configuration for analysis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
#from .views import StartRecordingView, StopRecordingView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('meet',views.meet),
    path('',views.home),
    path('home',views.home),
    path('meetlist',views.meetlist),
    path('meetoption',views.meetoption),
  path('start-recording/', views.start_recording, name='start_recording'),
    path('stop-recording/', views.stop_recording, name='stop_recording'),
]
