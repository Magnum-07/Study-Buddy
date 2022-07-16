from django.forms import ModelForm
from .models import Room, Message
from django.contrib.auth.models import User

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = "__all__"
        exclude = ['host', 'participants']
        
class MessageForm(ModelForm):
    def __init__(self, **kwargs):
        self.room = kwargs.pop('room', None)
        self.user = kwargs.pop('user', None)
        super(MessageForm, self).__init__(**kwargs)
        
    def save(self, commit=True):
        obj = super(MessageForm, self).save(commit=False)
        obj.room = self.room
        obj.user = self.user
        if commit:
            obj.save()
        return obj

    class Meta:
        model = Message
        fields = ['body']
        # fields = "__all__"

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']