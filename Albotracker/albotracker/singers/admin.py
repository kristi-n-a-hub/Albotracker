from django.contrib import admin
from .models import Singer
from .models import Genre


admin.site.register(Singer)
admin.site.register(Genre)