from django.shortcuts import render
from models.models import MusicItem, Link, Price
from rest_framework import serializers
from django.http import JsonResponse, FileResponse
from json import JSONEncoder
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from celery import Celery
from bs4 import BeautifulSoup
import re
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
app = Celery('tar')


def index(request):
    return render(request, './web_app.html')


class MusicItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicItem
        fields = ('name', 'image', 'pk')

    def to_representation(self, instance):
        super_s = super().to_representation(instance)
        super_s['increase'] = 0
        super_s['decrease'] = 0
        super_s['out_of_stock'] = 0
        super_s['in_stock'] = 0
        links = Link.objects.filter(parent=instance.pk)
        for link in links:
            if not link.unseen:
                continue
            history = Price.objects.filter(parent=link.pk).order_by('-created')[0:2]
            if (history.count() == 0):
                continue
            elif (history.count() == 1):
                super_s['increase'] += 1
            else:
                if history[history.count() - 1].value == -1:
                    super_s['in_stock'] += 1
                elif history[history.count() - 2].value == -1:
                    super_s['out_of_stock'] += 1
                elif history[history.count() - 2].value > history[history.count() - 1].value:
                    super_s['increase'] += 1
                elif history[history.count() - 2].value < history[history.count() - 1].value:
                    super_s['decrease'] += 1
        return super_s


class MusicItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicItem
        fields = ('name', 'image', 'url', 'pk')

    def to_representation(self, instance):
        super_s = super().to_representation(instance)
        links = Link.objects.filter(parent=instance.pk)
        serializer = LinkSerializer(links, many=True)
        super_s['links'] = serializer.data
        return super_s


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ('url', 'unseen', 'pk')

    def to_representation(self, instance):
        super_s = super().to_representation(instance)
        history = Price.objects.filter(parent=instance.pk).order_by('-created')[0:2]
        serializer = PriceSerializer(history, many=True)
        super_s['history'] = serializer.data
        if not instance.unseen:
            super_s['recent_change'] = 0
        elif (not instance.unseen or history.count() == 0):
            super_s['recent_change'] = 0
        elif (history.count() == 1):
            super_s['recent_change'] = history[0].value
        else:
            if history[history.count() - 2].value == -1:
                super_s['recent_change'] = -1
            elif history[history.count() - 1].value == -1:
                super_s['recent_change'] = -2
            else:
                super_s['recent_change'] = history[history.count() - 2].value - history[history.count() - 1].value
        return super_s


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ('value', 'created')


@csrf_exempt
@api_view(['POST'])
def musicItemHandler(request):
    if request.data["method"] == 'create':
        MusicItem.objects.create(
            name=request.data["name"], url=request.data["url"], image=request.data["image"])
        return JsonResponse({'success': True}, encoder=JSONEncoder)
    elif request.data["method"] == 'list':
        serializer = MusicItemListSerializer(MusicItem.objects.all(), many=True)
        return JsonResponse({'list': serializer.data, 'success': True}, encoder=JSONEncoder)
    elif request.data['method'] == 'get':
        serializer = MusicItemSerializer(MusicItem.objects.get(pk=request.data['pk']))
        return JsonResponse({'item': serializer.data, 'success': True}, encoder=JSONEncoder)
    elif request.data['method'] == 'delete':
        MusicItem.objects.get(pk=request.data['pk']).delete()
        return JsonResponse({'success': True}, encoder=JSONEncoder)
    elif request.data['method'] == 'update':
        item, created = MusicItem.objects. \
            update_or_create(pk=request.data['pk'],
                             defaults={'name': request.data["name"], 'url': request.data["url"],
                                       'image': request.data["image"]})
        return JsonResponse({'success': True}, encoder=JSONEncoder)
    elif request.data['method'] == 'seen':
        links = Link.objects.filter(parent=request.data['pk'])
        for link in links:
            link.unseen = False
            link.save()
        return JsonResponse({'success': True}, encoder=JSONEncoder)


@csrf_exempt
@api_view(['POST'])
def linkHandler(request):
    if (request.data['method'] == 'create'):
        parent = MusicItem.objects.get(pk=request.data['parent'])
        Link.objects.create(url=request.data['url'], parent=parent, unseen=False)
        return JsonResponse({'success': True}, encoder=JSONEncoder)
    elif (request.data['method'] == 'update'):
        item, created = Link.objects. \
            update_or_create(pk=request.data['pk'], defaults={'url': request.data['url']})
        return JsonResponse({'success': True}, encoder=JSONEncoder)
    elif (request.data['method'] == 'delete'):
        Link.objects.get(pk=request.data['pk']).delete()
        return JsonResponse({'success': True}, encoder=JSONEncoder)


@api_view(['GET'])
def fonta27a579bdf3c579fb0287ad7eedf13f5(request):
    return FileResponse(open('static/a27a579bdf3c579fb0287ad7eedf13f5.woff', 'rb'))


@api_view(['GET'])
def fontf9ada7e5233f3a92347b7531c06f2336(request):
    return FileResponse(open('static/f9ada7e5233f3a92347b7531c06f2336.woff2', 'rb'))


@api_view(['GET'])
def font655ba951f59a5b99d8627273e0883638(request):
    return FileResponse(open('static/655ba951f59a5b99d8627273e0883638.ttf', 'rb'))


def run_prices(request):
    get_prices()
    return JsonResponse({'success': True}, encoder=JSONEncoder)


@app.task
def get_prices():
    links = Link.objects.all()
    for link in links:

        site = re.findall("//(.*?)/", link.url)
        if site != []:
            price = Price.objects.create(parent=link)
            response = requests.get(link.url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            product = {
                "price": "00",
                "unit": "تومان",
            }

            # 1- iransote.com
            if site[0] == "iransote.com":
                p = soup.find("p", attrs={"class": "price"})
                if soup.find("p", attrs={"class": "stock out-of-stock"}) == None:
                    s = p.find("ins")
                    if s != None:
                        a = re.sub(r',', '', s.text).strip()
                    else:
                        a = re.sub(r',', '', p.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]

            # 2- iranloop.ir
            elif site[0] == "iranloop.ir":
                p = soup.find("p", attrs={"class": "our_price_display"})
                if soup.find("p", attrs={"id": "availability_statut"}).text == " موجود است":
                    s = p.find("span", attrs={"class": "price"})
                    if s != None:
                        a = re.sub(r',', '', s.text).strip()
                        b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]
                # print(product)

            # 3- www.sazforoosh.com
            elif site[0] == "www.sazforoosh.com":
                p = soup.find("div", attrs={"class": "price"})
                if soup.find("div", attrs={"id": "product"}).find('p'):
                    b = [""]
                else:
                    s = p.find("h3")
                    a = re.sub(r',', '', s.text).strip()
                    b = re.findall(r'\d+', a)
                product["price"] = b[0]
                # print(product)

            # 4- sazkala.com
            elif site[0] == "sazkala.com":
                p = soup.find("p", attrs={"class": "price"})
                if soup.find("div", attrs={"class": "absolute-label-product outofstock-product"}):
                    b = [""]
                else:
                    s = p.find("ins")
                    if s != None:
                        a = re.sub(r',', '', s.text).strip()
                    else:
                        a = re.sub(r',', '', p.text).strip()
                    b = re.findall(r'\d+', a)
                product["price"] = b[0]
                # print(product)

            # 5- sedastore.com
            elif site[0] == "sedastore.com":
                p = soup.find("p", attrs={"class": "price"})
                if soup.find("p", attrs={"class": "woocommerce-error"}) or soup.find("p",
                                                                                     attrs={"class": "price"}).find(
                    "strong"):
                    b = [""]
                else:
                    s = p.find("ins")
                    if s != None:
                        a = re.sub(r',', '', s.text).strip()
                    else:
                        a = re.sub(r',', '', p.text).strip()
                    b = re.findall(r'\d+', a)
                product["price"] = b[0]
                # print(product)

            # 6- www.djcenter.net
            elif site[0] == "www.djcenter.net":
                p = soup.find("span", attrs={"itemprop": "price"})
                if p != None:
                    s = re.sub(r'\s+', ' ', p.text).strip()
                    a = re.sub(r',', '', s)
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]
                # print(product)

            # 7- digiseda.ir
            elif site[0] == "digiseda.ir":
                p = soup.find("div", attrs={"id": "our_price_display", "class": "prd-price"})
                if p != None:
                    if soup.find("span", attrs={"id": "our_price_display", "class": "price"}) == None:
                        s = re.sub(r'\s+', ' ', p.text).strip()
                        a = re.sub(r',', '', s)
                        b = re.findall(r'\d+', a)
                    else:
                        b = [""]
                    product["price"] = b[0]
                # print(product)

            # 8- rayanseda.com
            elif site[0] == "rayanseda.com":
                p = soup.find("div", attrs={"class": "col-md-6 col-12 cost-product"})
                if p != None:
                    if p.find("span", attrs={"class": "row-off-cost"}):
                        s = p.find("span", attrs={"class": "row-off-cost"})
                    else:
                        s = p.find("span", attrs={"class": "prise-row orginal"})
                    a = re.sub(r',', '', s.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]
                # print(product)

            # 9- www.sornashop.com
            elif site[0] == "www.sornashop.com":
                p = soup.find("p", attrs={"class": "price"})
                if p != None:
                    if soup.find("p", attrs={"class": "stock out-of-stock"}) == None:
                        if p.find("ins") != None:
                            s = p.find("ins")
                        else:
                            s = p.find("bdi")
                        a = re.sub(r',', '', s.text).strip()
                        b = re.findall(r'\d+', a)
                    else:
                        b = [""]
                    product["price"] = b[0]
                # print(product)

            # 10- davarmelody.com
            elif site[0] == "davarmelody.com":
                if soup.find("div", attrs={"id": "product"}).find("p") == None:
                    p = soup.find("span", attrs={"itemprop": "price"})
                    s = re.sub(r'\s+', ' ', p.text).strip()
                    a = re.sub(r',', '', s)
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]
                # print(product)

            # 11- www.tehranmelody.com
            elif site[0] == "www.tehranmelody.com" or site[0] == "tehranmelody.software":
                if soup.find("button", attrs={"id": "button-cart"}):
                    p = soup.find("div", attrs={"class": "price"})
                    s = re.sub(r'\s+', ' ', p.text).strip()
                    a = re.sub(r',', '', s)
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]
                # print(product)

            # 12- navamarket.ir
            elif site[0] == "navamarket.ir":
                p = soup.find("span", attrs={"class": "price", "itemprop": "price"})
                if p.attrs['content'] == '1' or p.attrs['content'] == '4':
                    b = [""]
                else:
                    s = re.sub(r'\s+', ' ', p.text).strip()
                    a = re.sub(r',', '', s)
                    b = re.findall(r'\d+', a)
                product["price"] = b[0]
                # print(product)

            # 13- golhastore.ir
            elif site[0] == "golhastore.ir":
                p = soup.find("span", attrs={"class": "price", "itemprop": "price"})
                if p.text == 'لطفا تماس بگیرید.':
                    b = [""]
                else:
                    s = re.sub(r'\s+', ' ', p.text).strip()
                    a = re.sub(r',', '', s)
                    b = re.findall(r'\d+', a)
                product["price"] = b[0]
                # print(product)

            # 14- ertebat.co
            elif site[0] == "ertebat.co":
                if soup.find("span", attrs={"itemprop": "price"}):
                    p = soup.find("span", attrs={"itemprop": "price"})
                    s = re.sub(r'\s+', ' ', p.text).strip()
                    a = re.sub(r'\.', '', s)
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]
                # print(product)

            # 15- delshadmusic.com
            elif site[0] == "delshadmusic.com":
                if soup.find("button", attrs={"name": "add-to-cart"}):
                    p = soup.find("span", attrs={"class": "woocommerce-Price-amount amount"})
                    s = re.sub(r'\s+', ' ', p.text).strip()
                    a = re.sub(r',', '', s)
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]
                # print(product)

            # TODO compare price.value with lastprice of the same link
            price.value = product["price"]
            price.save()
            link.unseen = True
            link.save()
