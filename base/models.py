from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True) # even if the topic is not there room could still exists
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    
    updated = models.DateTimeField(auto_now=True) # this will update everytime when changes are made.
    created = models.DateTimeField(auto_now_add=True) # this will change only when iT's instance is created.
    
    class Meta:
        ordering = ['-updated', '-created']
    
    def __str__(self) -> str:
        return self.name
    
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE) # one to many relation -> as user can have many messages and one message can have only one user.
    body = models.CharField(max_length=200)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-updated', '-created']
    
    def __str__(self) -> str:
        return self.body[0:50]