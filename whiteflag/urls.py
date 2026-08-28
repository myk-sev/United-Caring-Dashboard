"""WhiteFlag URL configuration."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.flow_control, name="whiteflag"),
    path("submission", views.handle_submission, name="whiteflag_submission"),
    path("<int:pk>/", views.edit_page, name="whiteflag_edit"),
]
