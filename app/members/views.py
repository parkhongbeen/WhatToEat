import requests
import hiddenkey
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from members.forms import Loginform

User = get_user_model()
NAVER_ID = hiddenkey.naver_login_id
NAVER_SERECT = hiddenkey.naver_login_pw


def index(request):
    if request.User.is_authenticated:
        return redirect('restaurant:view_restaurant', page=1)
    return render(request, 'index.html')


def sign_up(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        if User.objects.filter(username=username).exists():
            return HttpResponse('이미 사용중인 username입니다.')
        if User.objects.filter(email=email).exists():
            return HttpResponse('이미 사용중인 email입니다.')

        user = User.objects.create_user(
            name=name,
            username=username,
            password=password,
            email=email,
        )

        login(request, user)
        return redirect('index')

    login_base_url = 'https://nid.naver.com/oauth2.0/authorize'
    login_params = {
        'response_type': 'code',
        'client_id': NAVER_ID,
        'redirect_url': 'http://localhost:8000/members/naver-login/',
        'state': 'RANDOM_STATE',
    }
    login_url = '{base}?{params}'.format(
        base=login_base_url,
        params='&'.join([f'{key}{value}' for key, value in login_params.items()]),
    )

    context = {
        'login_url': login_url,
    }

    return render(request, 'members.signup.html', context)


def log_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('index')
        else:
            return redirect('members:login')

    form = Loginform()

    login_base_url = 'https://nid.naver.com/oauth2.0/authorize'
    login_params = {
        'response_type': 'code',
        'client_id': NAVER_ID,
        'redirect_uri': 'http://localhost:8000/members/naver-login/',
        'state': 'RANDOM_STATE',
    }
    login_url = '{base}?{params}'.format(
        base=login_base_url,
        params='&'.join([f'{key}={value}' for key, value in login_params.items()])
    )

    context = {
        'form': form,
        'login_url': login_url,
    }

    return render(request, 'members/login.html', context)


def log_out(request):
    logout(request)
    return redirect('index')
