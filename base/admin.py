from django.contrib import admin

# Register your models here.
from . import models

myModels = [models.Room, models.Message, models.Topic]
admin.site.register(myModels)