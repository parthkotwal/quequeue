from django.urls import path
from . import views

urlpatterns = [
    path("health/", views.health),

    # LOGIN AND AUTHENTICATION
    path('login/', views.login),
    path('callback/', views.callback),
    path('verify_auth/', views.verify_auth),
    path('current_user/', views.current_user),
    path('get_token/', views.get_token),
    path("logout/", views.logout_view),
    path('transfer_player/', views.transfer_player),

    # PLAYBACK
    path('play_track/', views.play_track),
    path('pause_track/', views.pause_track),

    # EXPORT
    path('export_queue/', views.export_queue),
    path('cancel_export/', views.cancel_export),
    path("upload_image/", views.upload_image),

    # QUEUE CRUD FUNCTIONS
    path('queue/<int:queue_id>/get/', views.get_queue, name="get_queue"),
    path('queue/<int:queue_id>/update/', views.update_queue, name="update_queue"),
    path('queue/<int:queue_id>/delete/', views.delete_queue, name="delete_queue"),
    path('queue/<int:queue_id>/add_track/', views.add_track_to_queue, name="add_track"),
    path('queue/<int:queue_id>/remove_track/<int:track_id>/', views.remove_track_from_queue, name="remove_track"),


    # RESTORE QUEUE
    path('queue/<int:queue_id>/restore/', views.restore_queue),

    # ALL QUEUES
    path('my_queues/', views.my_queues),
    
    
    # SMART SUGGESTION
    path('queue/<int:queue_id>/suggest/', views.suggest),
    path('queue/<int:queue_id>/suggest_available/', views.suggest_available),
]