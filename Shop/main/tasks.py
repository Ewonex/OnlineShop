from celery import shared_task
import requests
from bs4 import BeautifulSoup
from io import BytesIO
from urllib.parse import urlencode
from .models import Item
from django.core.files import File
from celery import Celery
from datetime import timedelta

app = Celery('main')

@shared_task
def test_task():
    return "Celery is working!"

@app.task
def Scrap():
    print('started')
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


app.conf.beat_schedule = {
    'Scrap': {
        'task': 'main.tasks.Scrap',
        'schedule': timedelta(minutes=2)
    },
}