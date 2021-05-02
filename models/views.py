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

            # 16- delarammusic.com
            elif site[0] == "delarammusic.com":
                p = soup.find("span", attrs={"class": "text-success"})
                if p:
                    s = re.sub(r'\s+', ' ', p.text).strip()
                    a = re.sub(r',', '', s)
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]

            # 17- alikmusic.org
            elif site[0] == "alikmusic.org":
                if soup.find("button", attrs={"name": "add-to-cart"}):
                    p = soup.find("p", attrs={"class": "price"})
                    if p.find("ins") != None:
                        s = p.find("ins")
                    else:
                        s = p.find("bdi")
                    a = re.sub(r',', '', s.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]

            # 18- violincenter.ir
            elif site[0] == "violincenter.ir":
                if soup.find("button", attrs={"name": "add-to-cart"}):
                    p = soup.find("p", attrs={"class": "price"})
                    if p.find("ins") != None:
                        s = p.find("ins")
                    else:
                        s = p.find("bdi")
                    a = re.sub(r',', '', s.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]

            # 20- sedabazar
            elif site[0] == "donyayesazha.com":
                if soup.find("button", attrs={"name": "add-to-cart"}):
                    p = soup.find("p", attrs={"class": "price"})
                    if p.find("ins") != None:
                        s = p.find("ins")
                    else:
                        s = p.find("bdi")
                    a = re.sub(r',', '', s.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]

            # 20- sedabazar
            elif site[0] == "sedabazar.com":
                if soup.find("button", attrs={"id": "button-cart"}):
                    p = soup.find("ul", attrs={"class": "list-unstyled"}).findNext("ul")
                    s = p.find("h2")
                    a = re.sub(r',', '', s.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]

            # 21- www.hezarsoo.com
            elif site[0] == "www.hezarsoo.com":
                if soup.find("button", attrs={"class": "single_add_to_cart_button button alt"}) or soup.find("button",
                                                                                                             attrs={
                                                                                                                 "class": "single_add_to_cart_button button alt disabled wc-variation-selection-needed"}):
                    p = soup.find("p", attrs={"class": "price"})
                    if p.find("ins") != None:
                        s = p.find("ins")
                    else:
                        s = p.find("bdi")
                    a = re.sub(r',', '', s.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]

            # 22- fluteshop
            elif site[0] == "fluteshop.org":
                if soup.find("button", attrs={"name": "add-to-cart"}):
                    p = soup.find("p", attrs={"class": "price"})
                    if p.find("ins") != None:
                        s = p.find("ins")
                    else:
                        s = p.find("bdi")
                    a = re.sub(r',', '', s.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]


            # 23- digitalbaran.com
            elif site[0] == "digitalbaran.com":
                if soup.find("button", attrs={"class": "single_add_to_cart_button button alt"}) or soup.find("button",
                                                                                                             attrs={
                                                                                                                 "class": "single_add_to_cart_button button alt disabled wc-variation-selection-needed"}):
                    p = soup.find("span", attrs={"id": "ProductPrice"})
                    if p.find("ins") != None:
                        s = p.find("ins")
                    else:
                        s = p.find("bdi")
                    a = re.sub(r',', '', s.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]

            # 24- turingsanat.com
            elif site[0] == "turingsanat.com":
                if soup.find("button", attrs={"name": "add-to-cart"}):
                    p = soup.find("p", attrs={"class": "price"})
                    if p.find("ins") != None:
                        s = p.find("ins")
                    else:
                        s = p.find("bdi")
                    a = re.sub(r',', '', s.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]

            # 25- yerial.com
            elif site[0] == "yerial.com":
                if soup.find("button", attrs={"name": "add-to-cart"}):
                    p = soup.find("p", attrs={"class": "price"})
                    if p.find("ins") != None:
                        s = p.find("ins")
                    else:
                        s = p.find("bdi")
                    a = re.sub(r',', '', s.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]

            # 26- www.gostaresh-seda.com
            elif site[0] == "www.gostaresh-seda.com":
                if soup.find("span", attrs={"class": "btn disabled btn-green"}):
                    b = [""]
                else:
                    p = soup.find("div", attrs={"class": "pe", "style": "font-size:14px"})
                    if p.find("b") != None:
                        s = p.find("b")
                    a = re.sub(r',', '', s.text).strip()
                    b = re.findall(r'\d+', a)
                product["price"] = b[0]

            # 27- www.digikala.com
            elif site[0] == "www.digikala.com":
                if soup.find("div", attrs={"class": "c-product__seller-row c-product__seller-row--add-to-cart"}):
                    p = soup.find("div", attrs={"class": "c-product__seller-price-real"})
                    a = re.sub(r',', '', p.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]

            # 28- www.sazplaza.com
            elif site[0] == "www.sazplaza.com":
                if soup.find("button", attrs={"class": "single_add_to_cart_button button alt"}):
                    p = soup.find("p", attrs={"class": "price"})
                    if p.find("ins") != None:
                        s = p.find("ins")
                    else:
                        s = p.find("bdi")
                    a = re.sub(r',', '', s.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]

            # 29- www.kalaoma.com
            elif site[0] == "www.kalaoma.com":
                if soup.find("button",
                             attrs={"class": "km-btn km-theme-2 width-100 km-add-product-to-cart KM_addProductToCart"}):
                    p = soup.find("span", attrs={"itemprop": "price"})
                    a = re.sub(r',', '', p.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]


            # 30- jahanmelody.com
            elif site[0] == "jahanmelody.com":
                if soup.find("a", attrs={"id": "add-cart"}):
                    p = soup.find("span", attrs={"id": "price"})
                    a = re.sub(r',', '', p.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]


            # 31- echokowsar.com
            elif site[0] == "echokowsar.com":
                if soup.find("button", attrs={"class": "btn btn-primary flex-grow-1 flex-md-grow-0"}):
                    p = soup.find("h5", attrs={"itemprop": "offers"})
                    s = p.find("span")
                    a = re.sub(r',', '', s.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]

            # 32- sotplus.ir
            elif site[0] == "sotplus.ir":
                if soup.find("button", attrs={"class": "single_add_to_cart_button button alt"}):
                    p = soup.find("p", attrs={"class": "price"})
                    if p.find("ins") != None:
                        s = p.find("ins")
                    else:
                        s = p.find("bdi")
                    a = re.sub(r'\.', '', s.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]

            # 33- noornegar.com
            elif site[0] == "noornegar.com":
                if soup.find("button", attrs={"class": "single_add_to_cart_button button alt"}):
                    p = soup.find("p", attrs={"class": "price"})
                    if p.find("ins") != None:
                        s = p.find("ins")
                    else:
                        s = p.find("bdi")
                    a = re.sub(r',', '', s.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]

            # 34- www.artemusic.ir
            elif site[0] == "www.artemusic.ir":
                if soup.find("button", attrs={"class": "single_add_to_cart_button button alt"}):
                    p = soup.find("p", attrs={"class": "price"})
                    if p.find("ins") != None:
                        s = p.find("ins")
                    else:
                        s = p.find("span")
                    a = re.sub(r',', '', s.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]

            # 35- dgland.com
            elif site[0] == "dgland.com":
                p = soup.find("p", attrs={"class": "price"})
                if p:
                    p = soup.find("p", attrs={"class": "price"})
                    if p.find("ins") != None:
                        s = p.find("ins")
                    else:
                        s = p.find("span")
                    a = re.sub(r',', '', s.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]

            # 36- saaz24.com
            elif site[0] == "saaz24.com":
                if soup.find("button", attrs={"class": "single_add_to_cart_button button alt"}):
                    p = soup.find("p", attrs={"class": "price"})
                    if p.find("ins") != None:
                        s = p.find("ins")
                    else:
                        s = p.find("bdi")
                    a = re.sub(r',', '', s.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]

            # 37- melodinng.com
            elif site[0] == "melodinng.com":
                p = soup.find("p", attrs={"class": "price"})
                if p:
                    if p.find("ins") != None:
                        s = p.find("ins")
                    else:
                        s = p.find("bdi")
                    a = re.sub(r',', '', s.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]

            # 38- www.afrangdigital.com
            elif site[0] == "www.afrangdigital.com":
                if soup.find("button", attrs={"class": "button pro-add-to-cart"}):
                    p = soup.find("p", attrs={"class": "special-price"})
                    s = p.find("price")
                    a = re.sub(r',', '', s.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]

            # 39- parsiansote.com
            elif site[0] == "parsiansote.com":
                if soup.find("button", attrs={"name": "add-to-cart"}):
                    b = [""]
                else:
                    p = soup.find("span", attrs={"class": "price"})
                    if p.find("span", attrs={"class": "matrix_wolffinal-price"}):
                        s = p.find("span", attrs={"class": "matrix_wolffinal-price"})
                    else:
                        s = p.find("bdi")
                    a = re.sub(r',', '', s.text).strip()
                    b = re.findall(r'\d+', a)
                product["price"] = b[0]

            # 40- technicav.com
            elif site[0] == "technicav.com":
                if soup.find("button", attrs={"name": "add-to-cart"}):
                    p = soup.find("p", attrs={"class": "price"})
                    if p.find("ins") != None:
                        s = p.find("ins")
                    else:
                        s = p.find("bdi")
                    a = re.sub(r',', '', s.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]

            # 41- www.didnegar.com
            elif site[0] == "www.didnegar.com":
                if soup.find("button", attrs={"name": "add-to-cart"}):
                    p = soup.find("div", attrs={"class": "product-price fullsize"})
                    if p.find("ins") != None:
                        s = p.find("ins")
                    else:
                        s = p.find("bdi")
                    a = re.sub(r',', '', s.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]

            # 42- www.alijavadzadeh.com
            elif site[0] == "www.alijavadzadeh.com":
                if soup.find("button", attrs={"name": "add-to-cart"}):
                    p = soup.find("p", attrs={"class": "price"})
                    a = re.sub(r',', '', p.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]

            # 43- bia2piano.ir
            elif site[0] == "bia2piano.ir":
                if soup.find("button", attrs={"name": "add-to-cart"}):
                    p = soup.find("p", attrs={"class": "price"})
                    if p.find("ins") != None:
                        s = p.find("ins")
                    else:
                        s = p.find("bdi")
                    a = re.sub(r',', '', s.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]

            # 44- meghdadit.com
            # elif site[0] == "meghdadit.com":
            #     if soup.find("p", attrs={"class": "m-0"}):
            #         p = soup.find("span", attrs={"id": "lblPrice"})
            #         a = re.sub(r',', '', p.text).strip()
            #         b = re.findall(r'\d+', a)
            #     else:
            #         b = [""]
            #     product["price"] = b[0]

            # 45- sedamoon.com
            elif site[0] == "sedamoon.com":
                p = soup.find("p", attrs={"class": "price"})
                if p:
                    a = re.sub(r',', '', p.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]

            # 46- malltina.com
            elif site[0] == "malltina.com":
                if soup.find("button", attrs={"class": "btn-addToCart"}):
                    p = soup.find("div", attrs={"class": "final-price"})
                    s = p.find("strong")
                    a = re.sub(r',', '', s.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]

            # 47- pishgaman-seda
            elif site[0] == "pishgaman-seda.com":
                if soup.find("button", attrs={"name": "add-to-cart"}):
                    p = soup.find("p", attrs={"class": "price"})
                    if p.find("ins") != None:
                        s = p.find("ins")
                    else:
                        s = p.find("bdi")
                    a = re.sub(r',', '', s.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]

            # 48- www.dourbinet.com
            elif site[0] == "www.dourbinet.com":
                p = soup.find("span", attrs={"class": "price"})
                if p:
                    p = soup.find("span", attrs={"class": "price"})
                    a = re.sub(r',', '', p.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]

            # 49- avatasvir.com
            elif site[0] == "avatasvir.com":
                p = soup.find("p", attrs={"class": "price"})
                if p.text != "تماس بگیرید":
                    s = p.find("ins")
                    if s == None:
                        s = p.find("bdi")
                    if s != None:
                        a = re.sub(r',', '', s.text).strip()
                        b = re.split(r'\s', a)
                else:
                    b = [""]
                product["price"] = b[0]

            # 50- hilatel.ir
            elif site[0] == "hilatel.ir":
                p = soup.find("span", attrs={"itemprop": "price"})
                a = re.sub(r',', '', p.text).strip()
                b = re.split(r'\s', a)
                if b[0] == 'ناموجود':
                    b = [""]
                product["price"] = b[0]

            # 51- www.yamahairan.ir
            elif site[0] == "www.yamahairan.ir":
                p = soup.find("span", attrs={"class": "amount"})
                a = re.sub(r',', '', p.text).strip()
                b = re.split(r'\s', a)
                if b[0] == '۰':
                    b = [""]
                product["price"] = b[0]

            # 52- navakade.com
            elif site[0] == "navakade.com":
                if soup.find("button", attrs={"name": "add-to-cart"}):
                    p = soup.find("p", attrs={"class": "price"})
                    if p.find("ins") != None:
                        s = p.find("ins")
                    else:
                        s = p.find("bdi")
                    a = re.sub(r',', '', s.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]

            # 53- head-phone.ir
            elif site[0] == "head-phone.ir":
                p = soup.find("span", attrs={"class": "price"})
                if p:
                    a = re.sub(r',', '', p.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]

            # 54- touchmusic.ir
            elif site[0] == "touchmusic.ir":
                if soup.find("button", attrs={"name": "add-to-cart"}):
                    p = soup.find("p", attrs={"class": "price"})
                    if p.find("ins") != None:
                        s = p.find("ins")
                    else:
                        s = p.find("bdi")
                    a = re.sub(r',', '', s.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]

            # 55- www.ghesticlub.com
            elif site[0] == "www.ghesticlub.com":
                p = soup.find("div", attrs={"class": "defme"})
                if soup.find("input", attrs={"name": "sabad"}):
                    s = re.sub(r'\s+', ' ', p.text).strip()
                    a = re.sub(r',', '', s).strip()
                    b = re.split(r'\s', a)
                    if len(b) == 4:
                        b[0] = b[2]
                    elif b[0] == "تومان":
                        b[0] = ""
                    product["price"] = b[0]

            # 56- pcmaxhw.com
            elif site[0] == "pcmaxhw.com":
                if soup.find("button", attrs={"name": "add-to-cart"}):
                    p = soup.find("p", attrs={"class": "price"})
                    if p.find("ins"):
                        s = p.find("ins")
                        a = re.sub(r',', '', s.text).strip()
                    else:
                        a = re.sub(r',', '', p.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]

            # 57- www.pixel.ir
            elif site[0] == "www.pixel.ir":
                if soup.find("button",
                             attrs={"class": "btn btn-default btn-large add-to-cart btn-full-width btn-spin"}):
                    p = soup.find("div", attrs={"class": "current-price"})
                    a = re.sub(r',', '', p.text).strip()
                    b = re.findall(r'\d+', a)
                    if a == "تماس بگیرید":
                        b = [""]
                else:
                    b = [""]
                product["price"] = b[0]

            # 58- www.bokehland.com
            elif site[0] == "www.bokehland.com":
                p = soup.find("p", attrs={"class": "price"})
                if p == None or p.text == "":
                    b = [""]
                else:
                    s = p.find("span")
                    if s != None:
                        a = re.sub(r',', '', s.text).strip()
                        b = re.split(r'\s', a)
                        product["price"] = b[0]

            # 59- hajigame.ir
            elif site[0] == "hajigame.ir":
                p = soup.find("p", attrs={"class": "price"})
                if p == None or p.text == "":
                    b = [""]
                else:
                    if p.find("ins"):
                        s = p.find("ins")
                        a = re.sub(r',', '', s.text).strip()
                    else:
                        a = re.sub(r',', '', p.text).strip()
                    b = re.findall(r'\d+', a)
                    if a == "تماس بگیرید":
                        b = [""]
                product["price"] = b[0]

            # 60- janebi.com
            elif site[0] == "janebi.com":
                if soup.find("div", attrs={"class": "add-to-basket ripple-btn has-ripple add_to_basket"}):
                    p = soup.find("span", attrs={"id": "ProductPrice"})
                    a = re.sub(r',', '', p.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = ["0"]
                product["price"] = b[0]

            # 61- jeddikala.com
            elif site[0] == "jeddikala.com":
                if soup.find("button", attrs={"name": "add-to-cart"}):
                    p = soup.find("p", attrs={"class": "price"})
                    if p.find("ins"):
                        s = p.find("ins")
                        a = re.sub(r',', '', s.text).strip()
                    else:
                        a = re.sub(r',', '', p.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]

            # 62- didbartarshop.ir
            elif site[0] == "didbartarshop.ir":
                if soup.find("button", attrs={"name": "add-to-cart"}):
                    p = soup.find("p", attrs={"class": "price"})
                    if p.find("ins"):
                        s = p.find("ins")
                        a = re.sub(r',', '', s.text).strip()
                    else:
                        a = re.sub(r',', '', p.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]

            # 63- max-shop.ir
            elif site[0] == "max-shop.ir":
                if soup.find("span", attrs={"id": "buy"}):
                    p = soup.find("div", attrs={"class": "price"})
                    s = p.find("div")
                    a = re.sub(r',', '', s.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]


            # 64- www.pakhsh.shop
            elif site[0] == "www.pakhsh.shop":
                p = soup.find("div", attrs={"class": "price-wrapper"})
                if p != None:
                    s = p.find("ins")
                    if s == None:
                        a = re.sub(r',', '', p.text).strip()
                        b = re.split(r'\s', a)
                    else:
                        a = re.sub(r',', '', s.text).strip()
                        b = re.split(r'\s', a)
                else:
                    b = [""]
                product["price"] = b[0]



            # 65- www.safirkala.com
            elif site[0] == "www.safirkala.com":
                p = soup.find("p", attrs={"class": "price"})
                if p != None:
                    if p.find("ins"):
                        p = soup.find("p", attrs={"class": "price"}).find("ins")
                        s = re.sub(r'\s+', ' ', p.text).strip()
                        a = re.sub(r',', '', s).strip()
                        b = re.split(r'\s', a)
                        product["price"] = b[0]
                        product["unit"] = b[1]
                    else:
                        s = re.sub(r'\s+', ' ', p.text).strip()
                        a = re.sub(r',', '', s).strip()
                        b = re.split(r'\s', a)
                else:
                    b = [""]
                product["price"] = b[0]




            # 66- namacam.ir
            elif site[0] == "namacam.ir":
                p = soup.find("p", attrs={"class": "price"})
                if p != None:
                    s = p.find("ins")
                    if s == None:
                        s = p.find("bdi")
                    if s != None:
                        a = re.sub(r',', '', s.text).strip()
                        b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]



            # 67- www.akasisaatchi.com
            elif site[0] == "www.akasisaatchi.com":
                p = soup.find("p", attrs={"class": "price"})
                if p != None:
                    s = p.find("span")
                    if s != None:
                        a = re.sub(r',', '', s.text).strip()
                        b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]


            # 68- www.flashiran.net
            elif site[0] == "www.flashiran.net":
                p = soup.find("p", attrs={"class": "price"})
                if p != None:
                    s = p.find("ins")
                    if s == None:
                        s = p.find("bdi")
                    if s != None:
                        a = re.sub(r',', '', s.text).strip()
                        b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]



            # 69- mehragin.com
            elif site[0] == "mehragin.com":
                p = soup.find("span", attrs={"itemprop": "price"})
                if p != None:
                    a = re.sub(r',', '', p.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]


            # 70- barbadgallery.com
            elif site[0] == "barbadgallery.com":
                p = soup.find("p", attrs={"class": "price"})
                if p != None:
                    s = p.find("ins")
                    if s == None:
                        s = p.find("bdi")
                    if s != None:
                        a = re.sub(r',', '', s.text).strip()
                        b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]


            # 71- zirpele.ir
            elif site[0] == "zirpele.ir":
                p = soup.find("p", attrs={"class": "price"})
                if p != None:
                    s = p.find("ins")
                    if s == None:
                        s = p.find("span")
                    if s != None:
                        a = re.sub(r',', '', s.text).strip()
                        b = re.findall(r'\d+', a)
                        if a == 'تماس بگیرید':
                            b = [""]
                else:
                    b = [""]
                product["price"] = b[0]




            # 72- parsacam.com
            elif site[0] == "parsacam.com":
                p = soup.find("p", attrs={"class": "price"})
                if p != None:
                    s = p.find("ins")
                    if s == None:
                        s = p.find("bdi")
                    if s != None:
                        a = re.sub(r',', '', s.text).strip()
                        b = re.findall(r'\d+', a)
                        if a == 'تماس بگیرید':
                            b = [""]
                else:
                    b = [""]
                product["price"] = b[0]



            # 73- negahshop.com
            elif site[0] == "negahshop.com":
                p = soup.find("p", attrs={"class": "price"})
                if p != None:
                    s = p.find("ins")
                    if s == None:
                        s = p.find("bdi")
                    if s != None:
                        a = re.sub(r',', '', s.text).strip()
                        b = re.findall(r'\d+', a)
                        if a == 'تماس بگیرید':
                            b = [""]
                else:
                    b = [""]
                product["price"] = b[0]



            # 74- didgahstore.ir
            elif site[0] == "didgahstore.ir":
                p = soup.find("p", attrs={"class": "price"})
                if p != None:
                    s = p.find("ins")
                    if s == None:
                        s = p.find("bdi")
                    if s != None:
                        a = re.sub(r',', '', s.text).strip()
                        b = re.findall(r'\d+', a)
                        if a == 'تماس بگیرید':
                            b = [""]
                else:
                    b = [""]
                product["price"] = b[0]



            # 75- chavoosh110.com
            elif site[0] == "chavoosh110.com":
                p = soup.find("p", attrs={"class": "price"})
                if p != None:
                    s = p.find("ins")
                    if s == None:
                        s = p.find("bdi")
                    if s != None:
                        a = re.sub(r',', '', s.text).strip()
                        b = re.findall(r'\d+', a)
                        if a == 'تماس بگیرید':
                            b = [""]
                else:
                    b = [""]
                product["price"] = b[0]


            # 76- mobit.ir(موفق نشدم درستش کنم)
            # elif site[0] == "mobit.ir":
            #     p = soup.find("div" , attrs = {"class" : "product-summery v-card v-sheet v-sheet--outlined theme--light"})
            #     if p!= None:
            #         s = p.find("ins")
            #         a = re.sub(r',', '', s).strip()
            #         b = re.findall(r'\d+',a)
            #         if a == 'تماس بگیرید':
            #             b = [""]
            #     else:
            #         b = [""]
            #     product["price"] = b[0]

            # 77- edbazar.com(فرمول قیمت را بر می گرداند)
            elif site[0] == "edbazar.com":
                p = soup.find("ul", attrs={"ng-hide": "Good.Tender"})
                if p != None:
                    s = p.select("li span")
                    ss = re.sub(r'\s+', ' ', s[0].text).strip()
                    a = re.sub(r',', '', ss).strip()
                    b = re.findall(r'\d+', a)
                    if a == 'تماس بگیرید':
                        b = [""]
                else:
                    b = [""]
                product["price"] = b[0]





            # 78- saz-bazar.com
            elif site[0] == "saz-bazar.com":
                p = soup.find("div", attrs={"class": "current-price"})
                if p != None:
                    s = p.find("span", attrs={"itemprop": "price"})
                    # ss = re.sub(r'\s+', ' ', s[0].text).strip()
                    a = re.sub(r',', '', s.text).strip()
                    b = re.findall(r'\d+', a)
                    if a == 'تماس بگیرید':
                        b = [""]
                else:
                    b = [""]
                product["price"] = b[0]



            # 79- mahancamera.com
            elif site[0] == "mahancamera.com":
                p = soup.find("p", attrs={"class": "price"})
                if p != None:
                    s = p.find("strong")
                    if s != None:
                        a = re.sub(r',', '', s.text).strip()
                        b = re.findall(r'\d+', a)
                        if a == 'برای قیمت تماس بگیرید':
                            b = ["0"]
                else:
                    b = [""]
                product["price"] = b[0]



            # 80- avazac.com
            elif site[0] == "avazac.com":
                p = soup.find("p", attrs={"class": "price"})
                if p != None:
                    s = p.find("span")
                    if s != None:
                        a = re.sub(r',', '', s.text).strip()
                        b = re.findall(r'\d+', a)
                        if a == 'برای قیمت تماس بگیرید':
                            b = [""]
                else:
                    b = [""]
                product["price"] = b[0]


            # 81- exif.ir
            elif site[0] == "exif.ir":
                p = soup.find("p", attrs={"class": "price"})
                if p != None:
                    s = p.find("ins")
                    if s == None:
                        s = p.find("bdi")
                    if s != None:
                        a = re.sub(r',', '', s.text).strip()
                        b = re.findall(r'\d+', a)
                    else:
                        s = p.find("strong")
                        a = re.sub(r',', '', s.text).strip()
                        if a == 'تماس بگیرید':
                            b = [""]
                else:
                    b = [""]
                product["price"] = b[0]


            # 82- diddovom.com
            elif site[0] == "diddovom.com":
                p = soup.find("p", attrs={"class": "price"})
                if p != None:
                    s = p.find("ins")
                    if s == None:
                        s = p.find("bdi")
                    if s != None:
                        a = re.sub(r',', '', s.text).strip()
                        b = re.findall(r'\d+', a)
                    else:
                        b = [""]
                else:
                    b = [""]
                product["price"] = b[0]

            # 83- xn--ghbeb.com(کلا عکس است)

            # 84- classicshopper.ir
            elif site[0] == "classicshopper.ir":
                p = soup.find("div", attrs={"class": "item-newprice"})
                if p != None:
                    s = p.find("span")
                    if s != None:
                        a = re.sub(r',', '', s.text).strip()
                        b = re.findall(r'\d+', a)
                    if a == "تومان":
                        b = [""]
                else:
                    b = [""]
                product["price"] = b[0]

            # 85- golden8.ir
            elif site[0] == "golden8.ir":
                p = soup.find("p", attrs={"class": "price"})
                if p != None:
                    a = re.sub(r',', '', p.text).strip()
                    b = re.findall(r'\d+', a)
                    if a == "تومان":
                        b = [""]
                else:
                    b = [""]
                product["price"] = b[0]



            # 86- logilook.com
            elif site[0] == "logilook.com":
                p = soup.find("span", attrs={"itemprop": "price"})
                if p != None:
                    a = re.sub(r',', '', p.text).strip()
                    b = re.findall(r'\d+', a)
                    if a == "اتمام موجودی":
                        b = [""]
                else:
                    b = [""]
                product["price"] = b[0]



            # 87- lioncomputer.com
            elif site[0] == "lioncomputer.com":
                p = soup.find("div", attrs={"id": "product-price"})
                if p != None:
                    s = p.find("strong")
                    if s != None:
                        ss = re.sub(r'\s+', ' ', s.text).strip()
                        a = re.sub(r',', '', ss)
                        b = re.findall(r'\d+', a)
                        if a == "ناموجود":
                            b = [""]
                else:
                    b = [""]
                product["price"] = b[0]



            # 88- bobloseven.com
            elif site[0] == "bobloseven.com":
                p = soup.find("span", attrs={"class": "price"})
                if p != None:
                    a = re.sub(r',', '', p.text).strip()
                    b = re.findall(r'\d+', a)
                if soup.find("div", attrs={"class": "status"}):
                    s = soup.find("div", attrs={"class": "status"})
                    a = re.sub(r'\s+', '', s.text)
                if a == "ناموجود" or a == "بهزودی":
                    b = [""]
                product["price"] = b[0]




            # 89- kingbrand.ir
            elif site[0] == "kingbrand.ir":
                p = soup.find("h5", attrs={"class": "product-price"})
                if p != None:
                    s = re.sub(r'\s+', '', p.text).strip()
                    a = re.sub(r',', '', s)
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]




            # 90- timcheh.com
            elif site[0] == "timcheh.com":
                p = soup.find("span", attrs={"class": "product_styles_price__3Ws3t"})
                if p != None:
                    s = re.sub(r'\s+', '', p.text).strip()
                    a = re.sub(r',', '', s)
                    b = re.findall(r'\d+', a)
                if p.text == "":
                    b = [""]
                product["price"] = b[0]




            # 91- jskala.com
            elif site[0] == "jskala.com":
                p = soup.find("p", attrs={"class": "price"})
                if p != None:
                    s = p.find("ins")
                    if s == None:
                        s = p.find("bdi")
                    if s != None:
                        a = re.sub(r',', '', s.text).strip()
                        b = re.findall(r'\d+', a)
                    else:
                        b = [""]
                product["price"] = b[0]




            # 92- asarayan.com
            elif site[0] == "asarayan.com":
                p = soup.find("p", attrs={"class": "our_price_display"})
                if p != None:
                    a = re.sub(r',', '', p.text).strip()
                    b = re.findall(r'\d+', a)
                    if re.findall(r'^\D+', p.text)[0] == "ناموجود":
                        b = [""]
                product["price"] = b[0]
                # product["unit"] = "ریال"




            # 93- tehranspeaker.com
            elif site[0] == "tehranspeaker.com":
                p = soup.find("div", attrs={"class": "price-group"})
                if p != None:
                    s = p.find("div", attrs={"class": "product-price-new"})
                    if s == None:
                        a = re.sub(r',', '', p.text).strip()
                        b = re.findall(r'\d+', a)
                    else:
                        a = re.sub(r',', '', s.text).strip()
                        b = re.findall(r'\d+', a)
                product["price"] = b[0]



            # 94- technolife.ir
            elif site[0] == "technolife.ir":
                p = soup.find("h6")
                if p != None:
                    a = re.sub(r',', '', p.text).strip()
                    b = re.findall(r'\d+', a)
                product["price"] = b[0]




            # 95- mahgoni.com
            elif site[0] == "mahgoni.com":
                p = soup.find("p", attrs={"class": "price"})
                if p != None:
                    s = p.find("ins")
                    if s == None:
                        s = p.find("bdi")
                    if s != None:
                        a = re.sub(r',', '', s.text).strip()
                        b = re.findall(r'\d+', a)
                    else:
                        b = [""]
                product["price"] = b[0]




            # 96- avazonline.ir
            elif site[0] == "avazonline.ir":
                p = soup.find("div", attrs={"class": "price-wrapper"})
                if p != None:
                    if soup.find("p", attrs={"class": "stock out-of-stock"}) == None:
                        s = p.find("ins")
                        if s == None:
                            s = p.find("bdi")
                        if s != None:
                            a = re.sub(r',', '', s.text).strip()
                            b = re.findall(r'\d+', a)
                    else:
                        b = [""]
                product["price"] = b[0]




            # 97- zanbil.ir
            elif site[0] == "zanbil.ir":
                p = soup.find("div", attrs={"id": "product-price"})
                if p != None:
                    s = p.find("span", attrs={"itemprop": "price"})
                    if s != None:
                        ss = re.sub(r'\s+', '', s.text).strip()
                        a = re.sub(r',', '', ss)
                        b = re.findall(r'\d+', a)
                    else:
                        b = [""]
                product["price"] = b[0]
                # product["unit"] = "ریال"



            # 98- gilsara.com
            elif site[0] == "gilsara.com":
                p = soup.find("p", attrs={"class": "price"})
                if p != None:
                    if soup.find("p", attrs={"class": "stock out-of-stock"}) == None:
                        s = p.find("ins")
                        if s == None:
                            s = p.find("bdi")
                        if s != None:
                            a = re.sub(r',', '', s.text).strip()
                            b = re.findall(r'\d+', a)
                    else:
                        b = [""]
                product["price"] = b[0]



            # 99- esam.ir
            elif site[0] == "esam.ir":
                p = soup.find("span", attrs={"id": "ctl00_ctl00_main_main_LBLpriceIfDiscount"})
                if p.text != '':
                    a = re.sub(r',', '', p.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    s = soup.find("span", attrs={"id": "ctl00_ctl00_main_main_LBLprice"})
                    a = re.sub(r',', '', s.text).strip()
                    b = re.findall(r'\d+', a)
                product["price"] = b[0]




            # 100- bahartak.ir
            elif site[0] == "bahartak.ir":
                p = soup.find("p", attrs={"class": "price"})
                if p != None:
                    if soup.find("p", attrs={"class": "stock in-stock"}) != None:
                        s = p.find("ins")
                        if s == None:
                            s = p.find("bdi")
                        if s != None:
                            a = re.sub(r',', '', s.text).strip()
                            b = re.findall(r'\d+', a)
                    else:
                        b = [""]
                product["price"] = b[0]



            # 101- baniband.com
            elif site[0] == "baniband.com":
                p = soup.find("p", attrs={"class": "price"})
                if p != None:
                    if p.find("strong") == None:
                        s = p.find("ins")
                        if s == None:
                            s = p.find("bdi")
                        if s != None:
                            a = re.sub(r',', '', s.text).strip()
                            b = re.findall(r'\d+', a)
                    else:
                        b = [""]
                product["price"] = b[0]



            # 102- mahor.net
            elif site[0] == "mahor.net":
                p = soup.find("p", attrs={"class": "price"})
                if p != None:
                    if soup.find("p", attrs={"class": "stock out-of-stock"}) == None:
                        s = p.find("ins")
                        if s == None:
                            s = p.find("bdi")
                        if s != None:
                            a = re.sub(r',', '', s.text).strip()
                            b = re.findall(r'\d+', a)
                    else:
                        b = [""]
                product["price"] = b[0]



            # 103- emall.ir
            elif site[0] == "emall.ir":
                p = soup.find("p", attrs={"class": "price"})
                if p != None:
                    if soup.find("p", attrs={"class": "stock out-of-stock"}) == None:
                        s = p.find("ins")
                        if s == None:
                            s = p.find("bdi")
                        if s != None:
                            a = re.sub(r',', '', s.text).strip()
                            b = re.findall(r'\d+', a)
                    else:
                        b = [""]
                product["price"] = b[0]


            # 104- torob.com
            elif site[0] == "torob.com":
                p = soup.find("h2", attrs={"class": "jsx-1813026706"})
                if p != None:
                    s = re.sub(r'٫', '', p.text).strip()
                    a = re.sub(r'\s+', ' ', s)
                    b = re.findall(r'\d+', a)
                    if a == "ناموجود":
                        b = [""]
                product["price"] = b[0]




            # TODO compare price.value with lastprice of the same link
            price.value = product["price"]
            price.save()
            link.unseen = True
            link.save()
