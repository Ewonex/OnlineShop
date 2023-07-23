from django.urls import path, include
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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
