from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib import messages
from core.models import UserModule
from core.forms import SignupForm, LoginForm 
from django.views.decorators.http import require_POST
from django.contrib.auth import logout

def base(request):
    return render(request, 'core/base.html')

def about(request):
    return render(request, 'core/about.html')

def get_login_status(request):
    return JsonResponse({'is_logged_in': request.user.is_authenticated})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)  # Use the SignupForm
        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({'status': 'success', 'message': "Signup successful!"})
        return JsonResponse({'status': 'error', 'message': form.errors.as_json()})
    
    return JsonResponse({'status': 'error', 'message': "Invalid request."})

@require_POST
def login_view(request):
    form = LoginForm(request.POST)  # Use the LoginForm
    
    if form.is_valid():
        email = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(request, username=email, password=password)
        
        if user is not None and user.is_active:
            login(request, user)
            return JsonResponse({'status': 'success', 'message': "Login successful!"})
        else:
            return JsonResponse({'status': 'error', 'message': "Login failed. Check your email and password."})
    
    # If form is not valid, return errors as JSON
    return JsonResponse({'status': 'error', 'message': form.errors.as_json()}, safe=False)

@require_POST
def logout_view(request):
    logout(request)  # Log out the user
    return JsonResponse({'status': 'success', 'message': "Logged out successfully."})
