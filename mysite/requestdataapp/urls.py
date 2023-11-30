from django.urls import path

from .views import process_get_view, handle_file_upload, error_view

app_name = "requestdataapp"
urlpatterns = [
    path("get/", process_get_view, name="get_view"),
    path("upload/", handle_file_upload, name="file_upload"),
    path("error/", error_view, name="error_msg"),
]
