from threading import Thread

from django.shortcuts import render
from models.models import MusicItem, Link, Price, Customer
from rest_framework import serializers
from django.http import JsonResponse, FileResponse
from json import JSONEncoder
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from celery import Celery
import re
import logging
import datetime
import pytz
from constance import config
import time
import math
import sys
import time
import threading
import concurrent.futures
from models.apis import callCrawlerThread, callCrawlerThreadFast, reloadMusicItemPrice, test_link
from models.crawlers import www_donyayesaaz_com

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
app = Celery('donyasaaz')


def index(request):
    return render(request, './web_app.html')


class MusicItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicItem
        fields = ('name', 'image', 'pk', 'increase', 'decrease', 'out_of_stock', 'in_stock')


class MusicItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicItem
        fields = ('name', 'image', 'url', 'price', 'pk')

    def to_representation(self, instance):
        super_s = super().to_representation(instance)
        links = Link.objects.filter(parent=instance.pk).order_by('-unseen')
        serializer = LinkSerializer(links, many=True)
        decreased = sorted([x for x in serializer.data if x['recent_change'] < -2],
                           key=lambda k: k['history'][0]['value'])
        in_stock = sorted([x for x in serializer.data if x['recent_change'] == -1],
                          key=lambda k: k['history'][1]['value'])
        increased = sorted([x for x in serializer.data if x['recent_change'] > 0],
                           key=lambda k: k['history'][0]['value'])
        out_of_stock = sorted([x for x in serializer.data if x['recent_change'] == -2],
                              key=lambda k: k['history'][0]['value'])
        rest = sorted([x for x in serializer.data if x['recent_change'] == 0],
                      key=lambda k: math.inf if (len(k['history'])) == 0 else
                      k['history'][0]['value'] if k['history'][0]['value'] != -1 else sys.maxsize)
        super_s['links'] = decreased + in_stock + increased + out_of_stock + rest
        super_s['links'] = sorted(super_s['links'], key=lambda k: 0 if k['is_active'] else 1)
        return super_s


class LinkListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ('url', 'parent')


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ('url', 'unseen', 'pk', 'reported', 'is_active')

    def to_representation(self, instance):
        super_s = super().to_representation(instance)
        history = Price.objects.filter(parent=instance.pk).order_by('-created')[0:2]
        serializer = PriceSerializer(history, many=True)
        super_s['history'] = serializer.data
        if not instance.unseen:
            super_s['recent_change'] = 0
        elif history.count() == 0:
            super_s['recent_change'] = 0
        elif history.count() == 1:
            if history[0].value != -1:
                super_s['recent_change'] = history[0].value
            else:
                super_s['recent_change'] = -2
        else:
            if history[1].value == -1:
                super_s['recent_change'] = -1
            elif history[0].value == -1:
                super_s['recent_change'] = -2
            else:
                super_s['recent_change'] = history[0].value - history[1].value
        return super_s


class LinkHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ('url', 'parent')

    def to_representation(self, instance):
        super_s = super().to_representation(instance)
        history = Price.objects.filter(parent=instance.pk).order_by('-created')
        serializer = PriceSerializer(history, many=True)
        super_s['history'] = serializer.data
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
        import datetime
        from django.db.models import Q
        q = None
        if request.data['increase']:
            q = Q(increase__gt=0)
        if request.data['decrease']:
            q = q | Q(decrease__gt=0) if q is not None else Q(decrease__gt=0)
        if request.data['out_of_stock']:
            q = q | Q(out_of_stock__gt=0) if q is not None else Q(out_of_stock__gt=0)
        if request.data['in_stock']:
            q = q | Q(in_stock__gt=0) if q is not None else Q(in_stock__gt=0)
        page = request.data['page']
        pageSize = request.data['pageSize']
        if q is not None:
            queryset = MusicItem.objects.filter(q)
        else:
            queryset = MusicItem.objects.all()
        if request.data['sort_type'] == 1:
            queryset = queryset.order_by('-created')
        serializer = MusicItemListSerializer(queryset[page * pageSize: (page + 1) * pageSize], many=True)
        return JsonResponse({
            'list': serializer.data, 'total': queryset.count(),
            'lastCrawlStarted': config.lastCrawlStarted.strftime("%H:%M:%S")
            if config.lastCrawlStarted != 'None' else '',
            'lastCrawlEnded': config.lastCrawlEnded.strftime("%H:%M:%S")
            if type(config.lastCrawlEnded) is datetime.datetime else config.lastCrawlEnded,
            'lastCrawlChanges': config.lastCrawlChanges,
            'phoneNumberLastTime': config.phoneNumberLastTime.strftime("%H:%M:%S")
            if config.phoneNumberLastTime != 'None' else '' ,
            'phoneNumberTotal': config.phoneNumberTotal,
            'phoneNumberLatest': config.phoneNumberLatest,
            'success': True
        }, encoder=JSONEncoder)
    elif request.data['method'] == 'get':
        serializer = MusicItemSerializer(MusicItem.objects.get(pk=request.data['pk']))
        return JsonResponse({'item': serializer.data, 'success': True}, encoder=JSONEncoder)
    elif request.data['method'] == 'delete':
        MusicItem.objects.get(pk=request.data['pk']).delete()
        return JsonResponse({'success': True}, encoder=JSONEncoder)
    elif request.data['method'] == 'update':
        MusicItem.objects. \
            update_or_create(pk=request.data['pk'],
                             defaults={'name': request.data["name"], 'url': request.data["url"],
                                       'image': request.data["image"]})
        return JsonResponse({'success': True}, encoder=JSONEncoder)
    elif request.data['method'] == 'seen':
        links = Link.objects.filter(parent=request.data['pk'])
        for link in links:
            link.unseen = False
            link.save()
        musicItem = MusicItem.objects.get(pk=request.data['pk'])
        musicItem.increase = 0
        musicItem.decrease = 0
        musicItem.in_stock = 0
        musicItem.out_of_stock = 0
        musicItem.save()
        return JsonResponse({'success': True}, encoder=JSONEncoder)
    elif request.data['method'] == 'seen_all':
        links = Link.objects.all()
        for link in links:
            link.unseen = False
            link.save()
        musicItems = MusicItem.objects.all()
        for musicItem in musicItems:
            musicItem.increase = 0
            musicItem.decrease = 0
            musicItem.in_stock = 0
            musicItem.out_of_stock = 0
            musicItem.save()
        return JsonResponse({'success': True}, encoder=JSONEncoder)
    elif request.data['method'] == 'errors':
        from django.db.models import Q
        queryset = None
        if request.data['mode'] == 'error':
            queryset = Link.objects.filter(last_run=-2)
        elif request.data['mode'] == 'none':
            queryset = Link.objects.filter(Q(last_run=-1) | Q(last_run=None))
        elif request.data['mode'] == 'null':
            queryset1 = Link.objects.exclude(id__in=Price.objects.all().values_list('parent_id', flat=True))
            from datetime import datetime, timedelta
            last21Day = datetime.today() - timedelta(days=30)
            Q1 = Price.objects.filter(created__gte=last21Day).values_list('id', flat=True).distinct()
            Q2 = Price.objects.exclude(id__in=Q1).values_list('id', flat=True).distinct()
            queryset2 = Link.objects.exclude(~Q(id__in=Q2))
            queryset = (queryset1 | queryset2).distinct()
        serializer = LinkListSerializer(queryset, many=True)
        return JsonResponse({
            'list': serializer.data, 'total': queryset.count(), 'success': True
        }, encoder=JSONEncoder)


@csrf_exempt
@api_view(['POST'])
def linkHandler(request):
    if request.data['method'] == 'create':
        parent = MusicItem.objects.get(pk=request.data['parent'])
        Link.objects.create(url=request.data['url'], parent=parent, unseen=False)
        return JsonResponse({'success': True}, encoder=JSONEncoder)
    elif request.data['method'] == 'update':
        if 'url' in request.data:
            Link.objects. \
                update_or_create(pk=request.data['pk'], defaults={'url': request.data['url']})
        elif 'reported' in request.data:
            Link.objects. \
                update_or_create(pk=request.data['pk'], defaults={'reported': request.data['reported']})
        elif 'is_active' in request.data:
            Link.objects. \
                update_or_create(pk=request.data['pk'], defaults={'is_active': request.data['is_active']})
        return JsonResponse({'success': True}, encoder=JSONEncoder)
    elif request.data['method'] == 'delete':
        Link.objects.get(pk=request.data['pk']).delete()
        return JsonResponse({'success': True}, encoder=JSONEncoder)
    elif request.data['method'] == 'history':
        link = Link.objects.get(pk=request.data['pk'])
        return JsonResponse({'item': LinkHistorySerializer(link).data, 'success': True}, encoder=JSONEncoder)


@api_view(['GET'])
def fonta27a579bdf3c579fb0287ad7eedf13f5(request):
    return FileResponse(open('C:/Users/Administrator/Desktop/donyasaaz/static/a27a579bdf3c579fb0287ad7eedf13f5.woff', 'rb'))


@api_view(['GET'])
def fontf9ada7e5233f3a92347b7531c06f2336(request):
    return FileResponse(open('C:/Users/Administrator/Desktop/donyasaaz/static/f9ada7e5233f3a92347b7531c06f2336.woff2', 'rb'))


@api_view(['GET'])
def font655ba951f59a5b99d8627273e0883638(request):
    return FileResponse(open('C:/Users/Administrator/Desktop/donyasaaz/static/655ba951f59a5b99d8627273e0883638.ttf', 'rb'))


@app.task
def test():
    print('just a test')
    return JsonResponse({'success': True}, encoder=JSONEncoder)


@csrf_exempt
@api_view(['GET', 'POSt'])
def test_timezone(request):
    import datetime
    config.lastCrawlEnded = datetime.datetime.now(pytz.timezone('Asia/Tehran'))
    from models.crawlers import davarmelody_com
    class Object(object):
        pass

    a = Object()
    a.url = "https://davarmelody.com/zoom-g1x-four"
    print(davarmelody_com.davarmelody(a, headers, ""))
    return JsonResponse({'success': True}, encoder=JSONEncoder)


@csrf_exempt
@api_view(['GET'])
def create_and_download_backup(request):
    import subprocess
    from django.http.response import HttpResponse, HttpResponseRedirect
    import os
    import ctypes

    os.system('mysqldump -u root -pHolyDance donyasaaz > C:\\Users\\Administrator\\Desktop\\donyasaaz\\static\\dump.sql')
    # subprocess.call(['cmd', os.path.dirname(os.path.realpath(__file__)) + '\\mysqldump.sh'])
    response = HttpResponseRedirect('http://45.149.77.125/static/dump.sql')
    return response

@csrf_exempt
@api_view(['GET'])
def delete_temp(request):
    import subprocess
    from django.http.response import HttpResponse, HttpResponseRedirect
    import os
    import ctypes

    from pathlib import Path
    def rmdir(directory):
        directory = Path(directory)
        for item in directory.iterdir():
            if item.is_dir():
                try:
                    rmdir(item)
                except Exception as e:
                    print(e)
            else:
                try:
                    item.unlink()
                except Exception as e:
                    print(e)
        directory.rmdir()

    rmdir(Path("C:\\Windows\\Temp"))

    import os
    import ctypes

    free_bytes = ctypes.c_ulonglong(0)
    ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(u'c:\\'), None, None, ctypes.pointer(free_bytes))

    return JsonResponse({'success': True, 'space':free_bytes.value/(1024*1024*1024)}, encoder=JSONEncoder)

@csrf_exempt
@api_view(['GET'])
def free_space_left(request):
    import os
    import ctypes

    free_bytes = ctypes.c_ulonglong(0)
    ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(u'c:\\'), None, None, ctypes.pointer(free_bytes))

    return JsonResponse({'space':free_bytes.value/(1024*1024*1024)}, encoder=JSONEncoder)

@csrf_exempt
@api_view(['POST'])
def run_test_link(request):
    price = test_link(request.data['link'])
    return JsonResponse({'success': True, 'price': price}, encoder=JSONEncoder)


def run_tests(request):
    unitTest()
    return JsonResponse({'success': True}, encoder=JSONEncoder)


@csrf_exempt
@api_view(['POST'])
def run_prices(request):
    Thread(target=get_prices).start()
    return JsonResponse({'success': True}, encoder=JSONEncoder)

def run_divar(request):
    Thread(target=divar).start()
    return JsonResponse({'success': True}, encoder=JSONEncoder)

@csrf_exempt
@api_view(['POST'])
def run_prices_fast(request):
    Thread(target=get_prices_fast).start()
    return JsonResponse({'success': True}, encoder=JSONEncoder)


@csrf_exempt
@api_view(['POST'])
def run_reload_music_item_prices(request):
    Thread(target=reload_music_item_prices).start()
    return JsonResponse({'success': True}, encoder=JSONEncoder)


@app.task
def reload_music_item_prices():
    items = MusicItem.objects.all()
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as donyayesazz:
        for i in range(0, len(items)):
            donyayesazz.submit(reloadMusicItemPrice, items[i], i)


@app.task
def get_prices():
    config.lastCrawlStarted = datetime.datetime.now(pytz.timezone('Asia/Tehran'))
    config.lastCrawlChanges = 0
    Link.objects.all().update(last_run=None, last_run_started=None, last_run_ended=None)
    logger = logging.getLogger(__name__)
    statistic = {"TOTAL": 0}
    links = Link.objects.all().values('id', 'url').order_by('id')
    links = list(links)
    import random
    random.shuffle(links)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        for i in range(0, len(links)):
            site = re.findall("//(.*?)/", links[(i + 0) % len(links)]['url'])
            print(site)
            # time.sleep(15)
            if not site:
                logger.info('empty url :  %s,', str(links[(i + 0) % len(links)]['id']))
                continue
            pool.submit(callCrawlerThread, links[(i + 0) % len(links)], site, statistic, len(links))

    logger.info(statistic)

    config.lastCrawlEnded = datetime.datetime.now(pytz.timezone('Asia/Tehran'))
    logger.info('done')


def get_prices_fast():
    config.lastCrawlStarted = datetime.datetime.now(pytz.timezone('Asia/Tehran'))
    config.lastCrawlChanges = 0

    links = Link.objects.all()
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for i in range(0, len(links)):
            link = links[i]
            site = re.findall("//(.*?)/", link.url)
            if not site:
                continue
            pool.submit(callCrawlerThreadFast, link, site, i)

    config.lastCrawlEnded = datetime.datetime.now(pytz.timezone('Asia/Tehran'))

def divar():
    theAdds = []
    theCustomers = list(Customer.objects.all().values('phoneNumber'))
    import os
    from selenium import webdriver
    from bs4 import BeautifulSoup

    try:
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        # sys.path.append(os.path.abspath("chromedriver_95.exe"))
        # driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver_95.exe"), chrome_options=chrome_options)
        driver = webdriver.Chrome(executable_path="C:\\Users\\Administrator\\Desktop\\donyasaaz\\chromedriver.exe", chrome_options=chrome_options)
        driver.get("https://divar.ir/s/tehran/musical-instruments")
        time.sleep(10)
        driver.execute_script(
            "document.getElementsByClassName(\"kt-button kt-button--inlined kt-nav-button nav-bar__btn kt-nav-button--small\")[0].click()")
        time.sleep(5)
        driver.execute_script(
            "document.getElementsByClassName(\"kt-fullwidth-link kt-fullwidth-link--small navbar-my-divar__button-item\")[0].click()")
        time.sleep(5)
        (driver.find_elements_by_class_name("kt-textfield__input")[2]).send_keys("9359415518")
        time.sleep(60)
        (driver.find_elements_by_class_name("kt-textfield__input")[2]).send_keys(config.phoneNumberLatest)
        # time.sleep(5)
        # driver.execute_script(
        #     "document.getElementsByClassName(\"kt-button kt-button--primary auth-modal__submit-button\")[0].click()")
        time.sleep(10)
        driver.execute_script(
            "document.getElementsByClassName(\"kt-text-truncate kt-segments-item__label\")[1].click()")
        time.sleep(10)
        soup = BeautifulSoup(driver.page_source, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s', e)
        return None

    config.phoneNumberLastTime = datetime.datetime.now(pytz.timezone('Asia/Tehran'))
    config.phoneNumberTotal = 0
    config.phoneNumberLatest = ''
    firstAd = True
    while(True):
        adds = soup.find_all("a", attrs={"class": "kt-post-card kt-post-card--outlined kt-post-card--has-chat"})
        if len(adds) == 0:
            return -1
        for add in adds:
            if add['href'] in theAdds:
                continue
            else:
                theAdds.append(add['href'])
            try:
                driver.get("https://divar.ir"+add['href'])
                driver.execute_script("document.getElementsByClassName(\"kt-button kt-button--primary post-actions__get-contact\")[0].click()")
                if firstAd:
                    firstAd = False
                    time.sleep(5)
                    driver.execute_script(
                        "document.getElementsByClassName(\"kt-button kt-button--primary\")[2].click()")
                tries = 0
                while(True):
                    time.sleep(5)
                    tries = tries + 1
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    mobile = soup.find("a", attrs={"class": "kt-unexpandable-row__action kt-text-truncate ltr"})
                    if mobile is not None or tries >= 6:
                        break
                # driver.find_element(by=By.CLASS_NAME, value="kt-button kt-button--primary post-actions__get-contact").click()
                # WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, "kt-unexpandable-row__action kt-text-truncate ltr")))
                mobile = soup.find("a", attrs={"class":"kt-unexpandable-row__action kt-text-truncate ltr"})
                if mobile is None:
                    continue
                number = re.findall(r'\d+', mobile.text)
                if (len(number) == 0):
                    continue
                if number[0] in theCustomers:
                    continue
                else:
                    theCustomers.append(number[0])
                    # print(number[0])
                    customer = Customer.objects.create(phoneNumber=str(int(number[0])))
                    customer.save()
                    config.phoneNumberLastTime = datetime.datetime.now(pytz.timezone('Asia/Tehran'))
                    config.phoneNumberTotal = config.phoneNumberTotal + 1
                    config.phoneNumberLatest = number[0]
                    import zeep
                    wsdl = "https://www.payam-resan.com/ws/v2/ws.asmx?WSDL"
                    client = zeep.Client(wsdl=wsdl)
                    client.service.SendMessage(
                        Username="09122727100", PassWord="5e9K#p@6#3", MessageBodie="شماره کاربر: " + number[0],
                        RecipientNumbers=['9140510168'], SenderNumber="9999326216", Type=1,
                        AllowedDelay=0
                    )
                print(theCustomers)
            except Exception as e:
                print(e)
        time.sleep(300)
        try:
            driver.get("https://divar.ir/s/tehran/musical-instruments")
            time.sleep(8)
            soup = BeautifulSoup(driver.page_source, "html.parser")
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.info('%s', e)
            return None