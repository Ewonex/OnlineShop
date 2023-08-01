from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='main_page'),
    path('authorization', views.authorization, name='authorization_page'),
    path('registration', views.registration, name='registration_page'),
    path('logout', views.logout_user, name='logout'),
    path('catalog', views.catalogShow, name='catalog'),
    path('profile', views.profileShow, name='profile'),
    path('aboutUs', views.aboutUsShow, name='aboutUs'),
    path('clientCard', views.clientCardShow, name='clientCard'),
    path('giftCards', views.giftCardsShow, name='giftCards'),
    path('aboutItem<int:pk>', views.aboutItemShow.as_view(), name='aboutItem'),
    path('addToFavorites', views.addToFavorites, name='addToFavorites'),
    path('favorites', views.favoritesShow, name='favorites'),
    path('best', views.bestShow, name='best'),
    path('reviews', views.reviewsShow, name='reviews'),
    path('brands', views.brandsShow, name='brands'),
    path('vacansys', views.vacansysShow, name='vacansys'),
    path('garants', views.garantsShow, name='garants'),
    path('returnInfo', views.returnInfoShow, name='returnInfo'),
    path('returnBlank', views.returnBlankShow, name='returnBlank'),
    path('cart', views.cartShow, name='cart'),
    path('addToCart', views.addToCart, name='addToCart'),
    path('removeFromCart', views.removeFromCart, name='removeFromCart'),
    path('deleteFromCart', views.deleteFromCart, name='deleteFromCart'),
    path('createOrder', views.createOrder, name='createOrder'),
    path('news', views.newsShow, name='news'),
    path('sendTheReview', views.sendTheReview, name='sendTheReview'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
