from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserLoginForm, InterestForm, ChatMessageForm
from .models import Interest, ChatMessage

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('user_list')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('user_list')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('login')

@login_required
def user_list(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'user_list.html', {'users': users})

@login_required
def send_interest(request, user_id):
    receiver = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            interest = form.save(commit=False)
            interest.sender = request.user
            interest.receiver = receiver
            interest.save()
            return redirect('home')
    else:
        form = InterestForm(initial={'receiver': receiver})
    return render(request, 'send_interest.html', {'form': form, 'receiver': receiver})

@login_required
def view_interests(request):
    interests = request.user.received_interests.all()
    return render(request, 'view_interests.html', {'interests': interests})

@login_required
def chat(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    if not Interest.objects.filter(sender=request.user, receiver=other_user, accepted=True).exists() and \
       not Interest.objects.filter(sender=other_user, receiver=request.user, accepted=True).exists():
        return redirect('home')
    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.sender = request.user
            chat_message.receiver = other_user
            chat_message.save()
            return redirect('chat', user_id=user_id)
    else:
        form = ChatMessageForm()
    messages = ChatMessage.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by('timestamp')
    return render(request, 'chat.html', {'form': form, 'messages': messages, 'other_user': other_user})
