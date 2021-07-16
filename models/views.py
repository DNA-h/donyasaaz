from threading import Thread

from django.shortcuts import render
from models.models import MusicItem, Link, Price
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
    return FileResponse(open('static/a27a579bdf3c579fb0287ad7eedf13f5.woff', 'rb'))


@api_view(['GET'])
def fontf9ada7e5233f3a92347b7531c06f2336(request):
    return FileResponse(open('static/f9ada7e5233f3a92347b7531c06f2336.woff2', 'rb'))


@api_view(['GET'])
def font655ba951f59a5b99d8627273e0883638(request):
    return FileResponse(open('static/655ba951f59a5b99d8627273e0883638.ttf', 'rb'))


@app.task
def test():
    print('just a test')
    return JsonResponse({'success': True}, encoder=JSONEncoder)


@csrf_exempt
@api_view(['GET'])
def test_timezone(request):
    import datetime
    config.lastCrawlEnded = datetime.datetime.now(pytz.timezone('Asia/Tehran'))
    # from models.crawlers import sazkala_com
    # class Object(object):
    #     pass
    #
    # a = Object()
    # a.url = "https://sazkala.com/product/yamaha-psr-a350-%da%a9%db%8c%d8%a8%d9%88%d8%b1%d8%af/"
    # print(sazkala_com.sazkala(a, headers, ""))
    from datetime import datetime, timedelta
    result = app.debug_task.apply_async(countdown=10)
    result.get()
    return JsonResponse({'success': True}, encoder=JSONEncoder)

# @csrf_exempt
# @api_view(['GET'])
def create_and_download_backup():
    import subprocess
    from django.http.response import HttpResponse, HttpResponseRedirect

    subprocess.call(['sh', '../../mysqldump.sh'])
    response = HttpResponseRedirect('http://185.204.197.114/static/dump.sql')
    return response


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
    links = Link.objects.all().values('id','url').order_by('id')
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as pool:
        for i in range(0, len(links)):
            site = re.findall("//(.*?)/", links[i]['url'])
            if not site:
                logger.info('empty url :  %s,', str(links[i]['id']))
                continue
            pool.submit(callCrawlerThread, links[i], site, statistic, len(links))

    logger.info(statistic)

    config.lastCrawlEnded = datetime.datetime.now(pytz.timezone('Asia/Tehran'))
    logger.info('done')


def get_prices_fast():
    config.lastCrawlStarted = datetime.datetime.now(pytz.timezone('Asia/Tehran'))
    config.lastCrawlChanges = 0

    links = Link.objects.all()
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        for i in range(0, len(links)):
            link = links[i]
            site = re.findall("//(.*?)/", link.url)
            if not site:
                continue
            pool.submit(callCrawlerThreadFast, link, site, i)

    config.lastCrawlEnded = datetime.datetime.now(pytz.timezone('Asia/Tehran'))
