from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('create-room/', views.create_room, name="create-room"),
    path('update-room/<str:pk>/', views.update_room, name='update-room'),
    path('delete/<str:pk>/', views.delete_room, name="delete-room"),
    path('login/', views.user_login, name="user-login"),
    path('logout/',views.user_logout, name="user-logout"),
    path('register/', views.register_user, name="user-register"),
    path('user-profile/<str:pk>/', views.user_profile, name="user-profile"),
    path('delete-message/<str:pk>/', views.delete_message, name="delete-message"),
    path('update-message/<str:pk>/', views.update_message, name='update-message'),
    path('update-user/', views.update_user, name='update-user'),
    path('topic-page/', views.topic_page, name="topic-page"),
    path('activity-page/', views.activity_page, name="activity-page"),
]