from django.urls import path

from members.views import index, login

urlpatterns = [
    path('', index, name='index'),
    path('login/', login, name='login_page'),
]
