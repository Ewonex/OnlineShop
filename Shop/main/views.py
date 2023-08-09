from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files import File
from .models import Item, FavoriteItem, Review, Brand, Vacansy, ReturningRequest, BucketItem, Order, ItemOfTheOrder, Article
from .forms import RegistrationForm
from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView
from django.core.paginator import Paginator
import requests
from bs4 import BeautifulSoup
from io import BytesIO
from urllib.parse import urlencode
from elasticsearch import Elasticsearch

def index(request):
    data = {

    }
    return render(request, 'main/index.html', data)

def registration(request):
    error = []
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/authorization')
        else:
            for field, errors in form.errors.items():
                field_label = form.fields[field].label
                error.append(f"{field_label}: {', '.join(errors)}")
            error = ", ".join(error)
    form = RegistrationForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'main/registration.html', data)

def authorization(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main_page')
        else:
            error = 'Неверное имя пользователя или пароль'
            return render(request, 'main/authorization.html', {'error': error})
    else:
        return render(request, 'main/authorization.html')

def logout_user(request):
    logout(request)
    return redirect('main_page')

def catalogShow(request):
    search_query = ''
    items = Item.objects.order_by('id')
    if request.method == 'GET' and (request.GET.get('forMales', None) or request.GET.get('forFemales', None) or request.GET.get('onSale', None) or request.GET.get('searchBar')):
        if request.GET.get('searchBar'):
            search_query = request.GET.get('searchBar', '')
            items = items.filter(description__icontains=search_query.lower()) | Item.objects.filter(name__icontains=search_query.lower()) | Item.objects.filter(category__icontains=search_query.lower())
        else:
            if request.GET.get('onSale', None):
                items = items.filter(discount__gt=0)
            else:
                if request.GET.get('forMales', None):
                    items = items.filter(forMales=True)
                else:
                    items = items.filter(forFemales=True)
    else:
        if request.method == 'GET':
            fChildren = request.GET.get('forChildren')
            fMales = request.GET.get('forMales')
            fFemales = request.GET.get('forFemales')
            price_from = request.GET.get('priceFrom')
            price_to = request.GET.get('priceTo')
            onDiscount = request.GET.get('discount')
            # category = request.GET.get('category')
            if fChildren:
                items = items.filter(forChildren=True)
            if fMales:
                items = items.filter(forMales=True)
            if fFemales:
                items = items.filter(forFemales=True)
            if onDiscount:
                items = items.filter(discount__gt=0)
            if price_from and price_to:
                items = items.filter(price__gte=price_from, price__lte=price_to)
    paginator = Paginator(items, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    query_params = request.GET.copy()
    query_params.pop('page', None)

    data = {
        #'items': items,
        'query_params': urlencode(query_params),
        'items': page,
        'search_query': search_query
    }
    return render(request, 'main/catalog.html', data)


def profileShow(request):
    if request.user.is_anonymous:
        return redirect('/authorization')
    else:
        return render(request, 'main/profile.html')

def aboutUsShow(request):
    return render(request, 'main/aboutUs.html')

def clientCardShow(request):
    return render(request, 'main/clientCard.html')

def giftCardsShow(request):
    return render(request, 'main/giftCards.html')


class aboutItemShow(DetailView):
    model = Item
    template_name = 'main/aboutItem.html'
    context_object_name = 'item'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = context['item']
        context['stars'] = range(1, 6)
        context['reviews'] = Review.objects.filter(item=item).order_by('-mark')
        if self.request.user.is_authenticated:
            favorite_item = FavoriteItem.objects.filter(user=self.request.user, item=item).first()
            context['isFavorite'] = favorite_item
        return context

def addToFavorites(request):
    if request.method == 'POST' and request.user.is_authenticated:
        user = request.user
        itemId = request.POST.get('item_id')
        item = Item.objects.get(id=itemId)
        try:
            favorite_item = FavoriteItem.objects.get(user=user, item=item)
            favorite_item.delete()
        except FavoriteItem.DoesNotExist:
            favorite_item = FavoriteItem(user=user, item=item)
            favorite_item.save()
        return redirect(f'/aboutItem{itemId}')
    else:
        return redirect('/authorization')

def favoritesShow(request):
    if request.user.is_anonymous:
        return redirect('/authorization')
    else:
        user = request.user
        favorite_items = FavoriteItem.objects.filter(user=user)
        item_ids = favorite_items.values_list('item_id', flat=True)
        items = Item.objects.filter(id__in=item_ids)
        data = {
            'items': items
        }
        return render(request, 'main/favorites.html', data)

def bestShow(request):
    items = Item.objects.order_by('-mark')
    paginator = Paginator(items, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    data = {
        'items': page
    }
    return render(request, 'main/catalog.html', data)

def reviewsShow(request):
    reviews = Review.objects.order_by('-mark')
    paginator = Paginator(reviews, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    data = {
        'reviews': page,
        'stars': range(1, 6)
    }
    return render(request, 'main/reviews.html', data)

def brandsShow(request):
    brands = Brand.objects.order_by('id')
    data = {
        'brands': brands,
    }
    return render(request, 'main/brands.html', data)

def vacansysShow(request):
    vacansys = Vacansy.objects.order_by('id')
    data = {
        'vacansys': vacansys,
    }
    return render(request, 'main/vacansys.html', data)
def garantsShow(request):
    return render(request, 'main/garants.html')

def returnInfoShow(request):
    return render(request, 'main/returnInfo.html')

def returnBlankShow(request):
    if request.user.is_anonymous:
        return render(request, 'main/authorization.html')
    elif request.method == 'POST':
        item_id = request.POST.get('item')
        reason = request.POST.get('reason')
        try:
            item = Item.objects.get(pk=item_id)
            returning_request = ReturningRequest(user=request.user, item=item, text=reason)
            returning_request.save()
            return redirect('main_page')
        except Item.DoesNotExist:
            return render(request, 'main/returnBlank.html', {'error_message': 'Товар не найден'})
    else:
        return render(request, 'main/returnBlank.html')

def addToCart(request):
    if request.method == 'POST' and request.user.is_authenticated:
        user = request.user
        itemId = request.POST.get('item_id')
        item = Item.objects.get(id=itemId)
        try:
            bucketItem = BucketItem.objects.get(user=user, item=item)
            bucketItem.amount += 1
            bucketItem.save()
        except BucketItem.DoesNotExist:
            bucketItem = BucketItem(user=user, item=item)
            bucketItem.save()
        return redirect(f'/cart')
    else:
        return redirect('/authorization')

def removeFromCart(request):
    if request.method == 'POST' and request.user.is_authenticated:
        user = request.user
        itemId = request.POST.get('item_id')
        item = Item.objects.get(id=itemId)
        try:
            bucketItem = BucketItem.objects.get(user=user, item=item)
            bucketItem.amount -= 1
            bucketItem.save()
            if bucketItem.amount == 0:
                bucketItem.delete()
        except BucketItem.DoesNotExist:
            return redirect(f'/cart')
        return redirect(f'/cart')
    else:
        return redirect('/authorization')

def deleteFromCart(request):
    if request.method == 'POST' and request.user.is_authenticated:
        user = request.user
        itemId = request.POST.get('item_id')
        item = Item.objects.get(id=itemId)
        try:
            bucketItem = BucketItem.objects.get(user=user, item=item)
            bucketItem.delete()
        except BucketItem.DoesNotExist:
            return redirect(f'/cart')
        return redirect(f'/cart')
    else:
        return redirect('/authorization')

def cartShow(request):
    if request.user.is_anonymous:
        return redirect('/authorization')
    else:
        user = request.user
        cart = BucketItem.objects.filter(user=user)
        totalPrice = sum(item.item.discountPrice * item.amount for item in cart)
        data = {
            'cart': cart,
            'totalPrice': totalPrice
        }
        return render(request, 'main/cart.html', data)

def createOrder(request):
    if request.user.is_anonymous:
        return redirect('/authorization')
    else:
        if request.method == 'POST':
            user = request.user
            cart = BucketItem.objects.filter(user=user)
            totalPrice = sum(item.item.discountPrice * item.amount for item in cart)
            order = Order(user=user, totalPrice=totalPrice)
            order.save()
            for item in cart:
                itemOfTheOrder = ItemOfTheOrder(order=order, item=item.item, amount=item.amount, totalPrice=item.item.discountPrice * item.amount)
                itemOfTheOrder.save()
                item.delete()
        return redirect('/')

def newsShow(request):
    news = Article.objects.order_by('-dateOfPublish')
    data = {
        'news': news,
    }
    return render(request, 'main/news.html', data)

def sendTheReview(request):
    if request.user.is_anonymous:
        return redirect('/authorization')
    else:
        if request.method == 'POST':
            user = request.user
            itemId = request.POST.get('item_id')
            item = Item.objects.get(id=itemId)
            mark = request.POST.get('mark')
            text = request.POST.get('textOfRev')
            review = Review(user=user, item=item, mark=mark, text=text)
            review.save()
        return redirect('/')

def firstScrap(request):
    if request.user.is_superuser:
        for id in range(27509000, 27509100):
            response = requests.get(f'https://fh.by/product/{id}')
            if response.status_code == 200:
                #print(id)
                soup = BeautifulSoup(response.content, 'html.parser')
                no_stock_button = soup.find('button', text='Нет в наличии')
                if not no_stock_button:
                    name = soup.find('span', {'class': 'Product_desc__7j3VE'}).text.strip()
                    description = soup.find('p', {'class': 'Product_description__0cDEF'}).text.strip()
                    picUrl = soup.find('div', {'class': 'swiper-zoom-container'}).find('img')['src']
                    response = requests.get(picUrl)
                    picCont = BytesIO(response.content)

                    category = name.split()[0]

                    item = Item(name=name, description=description, category=category)
                    item.pic.save('image.jpg', File(picCont), save=True)

                    price = 0
                    try:
                        discount_tag = soup.find('div', {
                            'class': 'ProductFeature_sale___YGT_ ProductFeature_productFeature__HBw3O'})
                        if discount_tag:
                            item.discount = discount_tag.find('p').text.strip().replace('%', '')
                            price = soup.find('div', {
                                'class': 'Price_priceContainer__oBndf'}).find('div', {
                                'class': 'Price_font__eN9sO Price_oldPrice__sAYAY Price_newPrice__kec1A Price_fontProductPage__YsM_S'}).text.strip()[
                                    :-4].replace(',', '.').replace(' ', '')

                        price_container = soup.find('div', {'class': 'Price_priceContainer__oBndf'})
                        if price_container:
                            price_tag = price_container.find('div', {
                                'class': 'Price_font__eN9sO Price_oldPrice__sAYAY Price_fontProductPage__YsM_S'})
                            if price_tag:
                                price = price_tag.text.strip()[:-4].replace(',', '.').replace(' ', '')

                    except AttributeError:
                        price = 0

                    item.price = price

                    item.save()
                    print(f'{name} добавлен в бд')
    else:
        return redirect('/authorization')
    return redirect('/')

def delItems(request):
    if request.user.is_superuser:
        all_items = Item.objects.all()
        for item in all_items:
            item.delete()
    else:
        return redirect('/authorization')
    return redirect('/')

