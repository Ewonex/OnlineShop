from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout

from .models import Item, FavoriteItem
from .forms import RegistrationForm
from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView


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
            items = items.filter(description__icontains=search_query)
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
        else:
            if request.method == 'POST' and request.user.is_anonymous:
                return redirect('/authorization')
            else:
                print('добавлено в бакет')
                # добавление элемента в бакет
    for item in items:
        item.discount_price = item.price * ((100 - item.discount) / 100)
    data = {
        'items': items,
        'search_query': search_query
    }
    return render(request, 'main/catalog.html', data)


def profileShow(request):
    if request.user.is_anonymous:
        return redirect('main_page')
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
        if item.discount!=0:
            discounted_price = item.price * (1 - item.discount / 100)
            context['discounted_price'] = discounted_price
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
        for item in items:
            item.discount_price = item.price * ((100 - item.discount) / 100)
        data = {
            'items': items
        }
        return render(request, 'main/favorites.html', data)