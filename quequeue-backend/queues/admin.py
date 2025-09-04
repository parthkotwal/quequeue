from django.contrib import admin

# Register your models here.
from .models import User, Queue, Track

admin.site.register(User)
admin.site.register(Queue)
admin.site.register(Track)
