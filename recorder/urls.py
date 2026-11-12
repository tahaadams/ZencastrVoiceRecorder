from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path(
        "recordings/<int:recording_id>/download/",
        views.download_transcript,
        name="download_transcript",
    ),
]
