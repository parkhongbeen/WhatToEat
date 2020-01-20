from django.shortcuts import render


# Create your views here.
def view_restaurant(request):
    return render(request, 'view_restaurant.html')
