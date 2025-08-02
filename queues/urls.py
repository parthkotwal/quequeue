from django.urls import path
from . import views

urlpatterns = [
    # LOGIN AND AUTHENTICATION
    path('login/', views.login),
    path('callback/', views.callback),
    path('verify_auth/', views.verify_auth),
    path('current_user/', views.current_user, name="current_user"),

    # PLAYBACK
    path('play_track/', views.play_track),
    path('pause_track/', views.pause_track),

    # EXPORT
    path('export_queue/', views.export_queue, name="export_queue"),

    # QUEUE FUNCTIONS
    path('queue/<int:queue_id>/get/', views.get_queue, name="get_queue"),
    path('queue/<int:queue_id>/update/', views.update_queue, name="update_queue"),
    path('queue/<int:queue_id>/delete/', views.delete_queue, name="delete_queue"),
    path("upload_image/", views.upload_queue_image, name="upload_image"),

    # RESTORE QUEUE
    path('restore_queue/<int:queue_id>/', views.restore_queue),

    # ALL QUEUES
    path('my_queues/', views.my_queues, name="my_queues"),
    
    # SMART SUGGESTION
    path('suggest/<int:queue_id>/', views.smart_suggestions, name='smart_suggestions'),
]