import datetime
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import SignUpForm
from .models import Image, Profile
from .forms import  ImageUploadForm
from django.shortcuts import render, redirect
from .forms import UserDetailForm, ProfileForm
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me', False)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = redirect('home')
            if remember_me:
                max_age = 30 * 24 * 60 * 60
                expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
                response.set_cookie('username', username, max_age=max_age, expires=expires, secure=False, httponly=True)
                response.set_cookie('password', password, max_age=max_age, expires=expires, secure=False, httponly=True)
            return response
        else:
            messages.error(request, "用户名或密码不正确")
    return render(request, 'accounts/login.html')

def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'accounts/register.html', {'form': form})



def home(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_img = Image(image=request.FILES['image'])
            new_img.save()

            return redirect('home')
    else:
        form = ImageUploadForm()
    images = Image.objects.all()
    return render(request, 'accounts/home.html', {'form': form, 'images': images})


@login_required
def userinfo_view(request):
    if request.method == 'POST':
        user_form = UserDetailForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('userinfo')
    else:
        user_form = UserDetailForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'accounts/userinfo.html', context)
