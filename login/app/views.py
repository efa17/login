from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from .models import User
from .forms import RegisterForm, LoginForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_verified = False
            user.set_password(form.cleaned_data['password'])
            user.generate_otp()
            user.save()
            send_mail(
                'Your OTP Code',
                f'Your OTP is {user.otp}',
                None,
                [user.email]
            )
            return render(request, 'otp_popup.html', {'email': user.email})
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

@csrf_exempt
def verify_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = request.POST.get('otp')
        try:
            user = User.objects.get(email=email)
            if user.otp == otp:
                user.is_verified = True
                user.save()
                login(request, user)
                return JsonResponse({'success': True})
            return JsonResponse({'success': False, 'message': 'Invalid OTP'})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found'})

@csrf_exempt
def resend_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            user.generate_otp()
            send_mail(
                'Resend OTP Code',
                f'Your OTP is {user.otp}',
                None,
                [user.email]
            )
            return JsonResponse({'success': True})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found'})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['email_or_phone']
            password = form.cleaned_data['password']
            user = User.objects.filter(email=identifier).first() or User.objects.filter(phone=identifier).first()
            if user and user.check_password(password):
                if user.is_verified:
                    login(request, user)
                    return redirect('home')
                else:
                    return render(request, 'otp_popup.html', {'email': user.email})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

from django.contrib.auth.decorators import login_required

@login_required
def home_view(request):
    return render(request, 'home.html')
