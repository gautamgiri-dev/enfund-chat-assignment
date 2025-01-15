import json
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login as auth_login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Message
from .forms import SimpleUserCreationForm

def not_authenticated(user):
    return not user.is_authenticated

def get_user_by_username(username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None
    return user

def get_all_users(current_user):
    users = User.objects.exclude(id=current_user.id)
    
    # You can transform the users into a list of dictionaries if needed
    user_list = [
        {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name
        } 
        for user in users
    ]
    
    return user_list

def index(request):
    context = {}
    if request.user.is_authenticated:
        # Get the list of users excluding the currently logged-in user
        users = get_all_users(request.user)
        context['users'] = users  # Add users to the context
    return render(request, "index.html", context)

@user_passes_test(not_authenticated, login_url='chat')
def login(request):
    context = dict()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login successful!")
            return redirect('/') 
        else:
            context['error'] = "Invalid username or password. Please try again."

    return render(request, "login.html", context=context)

@user_passes_test(not_authenticated, login_url='chat')
def register(request):
    if request.method == 'POST':
        form = SimpleUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created successfully!")
            return redirect('login')
    else:
        form = SimpleUserCreationForm()
    return render(request, 'register.html', {'form': form})

# Ensure the user is logged in to access the chat page
@login_required(login_url='login')
def chat(request):
    context = dict()
    users = get_all_users(request.user)
    context['users'] = users

    receiver_username = request.GET.get('user', None)
    if not receiver_username:
        return redirect('/')
    
    receiver = get_user_by_username(receiver_username)
    if not receiver or receiver.username == request.user.username:
        return redirect('/')
    
    context['receiver'] = receiver

    return render(request, "chat.html", context=context)

@csrf_exempt
@login_required(login_url='login')
def get_messages(request):
    # TODO: this view should support pagination for scalability
    receiver_username = request.GET.get('user', None)
    if not receiver_username:
        return redirect('/')
    
    receiver = get_user_by_username(receiver_username)
    if not receiver or receiver.username == request.user.username:
        return redirect('/')
    
    '''
        Response object should be of following structure
        [    
            {
                'type': 'sent',
                'content': 'Hello',
                'timestamp': '145488555'
            },
            {
                'type': 'received',
                'content': 'Hello',
                'timestamp': '5464654654654'
            },
        ]
    '''

    messages = Message.objects.filter(sender=request.user, receiver=receiver) | Message.objects.filter(sender=receiver, receiver=request.user)
    messages = messages.order_by('timestamp')
    messages_list = [
        {
            'type': 'sent' if message.sender == request.user else 'received',
            'content': message.message,
            'timestamp': message.timestamp.timestamp()
        }
        for message in messages
    ]
    return JsonResponse(messages_list, safe=False)

@csrf_exempt
@login_required(login_url='login')
def send_message(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        receiver_username = body.get('to', None)
        message = body.get('message', None)
        print(receiver_username, message)
        if not receiver_username or not message:
            return JsonResponse({'error': 'Invalid request'}, status=400)
        
        receiver = get_user_by_username(receiver_username)
        if not receiver or receiver.username == request.user.username:
            return JsonResponse({'error': 'Invalid request'}, status=400)
        
        Message.objects.create(sender=request.user, receiver=receiver, message=message)
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)

# Logout view
@login_required(login_url='login')
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('/')