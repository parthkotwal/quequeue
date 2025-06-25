from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login),
    path('callback/', views.callback),
    path('verify_auth/', views.verify_auth, name='verify_auth'),
    path('current_user/', views.current_user, name="current_user"),
    path('export_queue/', views.export_queue, name="export_queue"),
    path('restore_queue/<int:queue_id>/', views.restore_queue),
    path('my_queues/', views.my_queues, name="my_queues"),
    path('queue/<int:queue_id>/details/', views.get_queue_details),
    path("upload_image/", views.upload_queue_image, name="upload_image"),
    path('suggest/<int:queue_id>/', views.smart_suggestions, name='smart_suggestions'),
]