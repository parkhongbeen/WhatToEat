from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.shortcuts import render, redirect
from restaurant.models import Restaurant


# Create your views here.
def view_restaurant(request, page=None):
    if request.method == 'POST' or page == '2':
        keyword = request.post['search_word']

        # 키워드를 cp949 형태로 인코딩
        cp949_keyword = keyword.encode('cp949')
        encoding_keyword = str(cp949_keyword)[2:-1].replace('\\x', '%')

        url = f'https://www.menupan.com/search/restaurant/restaurant_result.asp?sc=basicdata&kw={encoding_keyword}&page={page}'
        response = request.get(url)
        html = BeautifulSoup(url.text)

        shop = html.select_one('ul.listStyle3')
        shop_list = shop.select('li')
        result_list = []

        for shop in shop_list:
            src = shop.select_one('img')
            link = shop.select_one('a')['href=']
            title = shop.select_one('dl a').get_text()
            category, menu = shop.select_one('dd').get_text().split(' |')
            address = text[0]
            tel = text[1]

            shop_dict = {
                'title': title,
                'src': src,
                'link': link,
                'category': category,
                'menu': menu,
                'tel': tel,
                'address': address
            }

            result_list.append(shop_dict)

        context = {
            'result_list': result_list,
            'search_world': request.POST['search_world'],
        }

        return render(request, 'index.html', context)
    else:
        return render(request, 'index.html')


def bookmark(request):
    title = request.POST['title']
    src = request.POST['src']
    link = request.POST['link']
    category = request.POST['category']
    menu = request.POST['menu']
    tel = request.POST['tel']
    address = request.POST['address']

    restaurant = Restaurant.objects.get_or_create(title=title, src=src, link=link, category=category,
                                                  menu=menu, tel=tel, address=address)
    restaurant.user.add(request.user)

    return HttpResponse('<script>window.onload = function(){alert("즐겨찾기에 추가 되었습니다."); history.back();}</script>')


def bookmark_list(request):
    if request.user.is_authenticated:

        result_list = Restaurant.objects.filter(user=request.user)
        context = {
            'result_list': result_list
        }
        return render(request, 'restaurant/bookmark_list.html', context)
    else:
        return redirect('login')


def bookmark_delete(request, pk):
    restaurant = Restaurant.objects.get(pk=pk)
    restaurant.delete()

    return redirect('restaurant:bookmark_list')
