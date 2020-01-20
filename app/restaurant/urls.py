from django.urls import path

from restaurant.views import view_restaurant

app_name = 'restaurant'
urlpatterns = [
    path('restaurant/<int:page>', view_restaurant, name='view_restaurant'),
]
