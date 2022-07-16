from .models import Room, Topic, Message
from .forms import RoomForm, MessageForm, UserForm
from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
# Create your views here.

class customError(Exception):
    pass

def user_login(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        # user = User.objects.get_or_create(username=username)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "User doesn't exists.")
            return redirect('user-login')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password doesn't match!.")
    context = {'page':page}
    return render(request, 'base/login_register.html', context)


def user_logout(request):
    logout(request)
    return redirect('home')

def register_user(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            # if User.objects.filter(username=user.username).exists():
            #     messages.error(request, "User already exists.")
            #     return redirect('user-register')
            # user.save()
            # login(request, user)
            # return redirect('home')
            try:
                user = User.objects.get(username=user.username)
                messages.error(request, "User already Exists")
            except User.DoesNotExist: 
                user.save()
                login(request, user)
                return redirect('home')
            # messages.error(request, "User already exists.")
            # return redirect('user-register')
        else:
            messages.error(request, 'An unknown error occured!')
    
    return render(request, 'base/login_register.html', {'form':form})
    
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains = q) |
        Q(description__icontains = q) 
        )
    
    topics = Topic.objects.filter(
        Q(room__gte =0)
    ).distinct()[0:5]
    # topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q)
    )
    # room_messages = Message.objects.all()
    context = {'rooms': rooms, 'topics': topics, 'room_count':room_count, 'room_messages':room_messages}
    return render(request,'base/home.html', context)


def room(request, pk): # this is used for editing a message too in room_html field
    found = Room.objects.get(id=int(pk))
    room_messages = found.message_set.all()
    participants = found.participants.all()
    form = MessageForm()
    if request.method == "POST":
        form = MessageForm(user = request.user, room = found, data = request.POST)
        if form.is_valid():
            data = form.save(commit = False)
            found.participants.add(data.user)
            data.save()
            return redirect('room', pk=found.id)
    
    context = {'rooms': found, 'room_messages':room_messages, 'participants':participants, 'forms':MessageForm}
    return render(request,'base/room.html', context)

def user_profile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.filter(
        Q(room__gte =0)
    )
    context = {'user':user, 'rooms':rooms, 'room_messages':room_messages, 'topics':topics}
    return render(request, 'base/profile.html', context)

@login_required(login_url="user-login")
def update_message(request, pk):
    # found = Room.objects.get(id=pk)
    message = Message.objects.get(id=pk)
    temp = message.room.id
    found = Room.objects.get(id=temp)
    participants = message.room.participants.all()
    room_messages = message.room.message_set.all().order_by('created')
    form = MessageForm(instance=message)
    
    if request.user != message.user:
        return HttpResponse("You are not allowed here!")
    
    if request.method == "POST":
        form = MessageForm(user = request.user, room = message.room, data = request.POST, instance=message)
        if form.is_valid:
            form.save()
            return redirect('room', pk=temp)
    
    context = {'rooms':found, 'forms': form, 'room_messages':room_messages, 'participants':participants}
    return render(request, 'base/room.html', context)

@login_required(login_url="user-login")
def delete_message(request, pk):
    message = Message.objects.get(id=pk)
    
    if request.user != message.user:
        return HttpResponse("You are not allowed here!")
    
    if request.method == "POST":
        message.delete()

        return redirect('home')
        
    string = "message"
    context = {'obj':message, 'message':string }
    return render(request, 'base/delete.html', context)

@login_required(login_url="user-login")
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()
    
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        return redirect('home')
    context = {'forms': form, 'topics':topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url="user-login")
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    
    if request.user != room.host:
        return HttpResponse("You are not allowed here!")
    
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')    
        room.description = request.POST.get('description')    
        room.topic = topic
        room.save()    
        return redirect('home')
    
    context = {'forms':form, 'topics':topics, 'room':room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url="user-login")
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    
    if request.user != room.host:
        return HttpResponse("You are not allowed here!")
    
    if request.method == "POST":
        room.delete()
        return redirect('home')
        
    context = {'obj':room}
    return render(request, 'base/delete.html', context)


@login_required(login_url="user-login")
def update_user(request):
    user = request.user
    form = UserForm(instance=user)
    
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    
    
    return render(request, 'base/update_user.html', {'forms':form})

def topic_page(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(
        Q(name__icontains=q),
        Q(room__gte = 0)
    ).distinct()
    
    context = {'topics':topics}
    return render(request, 'base/topics.html', context)


def activity_page(request):
    
    room_messages = Message.objects.all()
    
    return render(request, 'base/activity_page.html', {'room_messages': room_messages})