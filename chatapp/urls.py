from django.urls import path
from . import views


    
urlpatterns = [
    path('', views.user_list, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('users/', views.user_list, name='user_list'),
    path('send_interest/<int:user_id>/', views.send_interest, name='send_interest'),
    path('view_interests/', views.view_interests, name='view_interests'),
    path('chat/<int:user_id>/', views.chat, name='chat'),
]
