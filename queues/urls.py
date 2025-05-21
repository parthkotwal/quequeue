from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login),
    path('callback/', views.callback),
    path('export_queue/', views.export_queue, name="export_queue"),
    path('restore_queue/<int:queue_id>/', views.restore_queue, name="restore_queue"),
    path('my_queues/', views.list_user_queues, name="list_user_queues"),
    path("upload_image/", views.upload_queue_image, name="upload_image"),
]