from threading import Thread

from django.shortcuts import render
from models.crawlers import *
from models.models import MusicItem, Link, Price
from rest_framework import serializers
from django.http import JsonResponse, FileResponse
from json import JSONEncoder
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from celery import Celery
import re
from constance import config

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
app = Celery('tar')


def index(request):
    return render(request, './web_app.html')


class MusicItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicItem
        fields = ('name', 'image', 'pk', 'increase', 'decrease', 'out_of_stock', 'in_stock')


class MusicItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicItem
        fields = ('name', 'image', 'url', 'pk')

    def to_representation(self, instance):
        super_s = super().to_representation(instance)
        links = Link.objects.filter(parent=instance.pk).order_by('-unseen')
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
        elif not instance.unseen or history.count() == 0:
            super_s['recent_change'] = 0
        elif history.count() == 1:
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
        serializer = MusicItemListSerializer(
            MusicItem.objects.all().order_by('out_of_stock').order_by('in_stock')
                .order_by('-decrease').order_by('-increase'), many=True)
        return JsonResponse({
            'list': serializer.data,
            'lastCrawlStarted': config.lastCrawlStarted.strftime("%H:%M:%S")
                if config.lastCrawlStarted != 'None' else '',
            'lastCrawlEnded': config.lastCrawlEnded.strftime("%H:%M:%S")
                if config.lastCrawlEnded != 'None' else '',
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


@csrf_exempt
@api_view(['POST'])
def linkHandler(request):
    if request.data['method'] == 'create':
        parent = MusicItem.objects.get(pk=request.data['parent'])
        Link.objects.create(url=request.data['url'], parent=parent, unseen=False)
        return JsonResponse({'success': True}, encoder=JSONEncoder)
    elif request.data['method'] == 'update':
        Link.objects. \
            update_or_create(pk=request.data['pk'], defaults={'url': request.data['url']})
        return JsonResponse({'success': True}, encoder=JSONEncoder)
    elif request.data['method'] == 'delete':
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


def test_timezone(request):
    import datetime
    return JsonResponse({'success': datetime.datetime.now().__str__()}, encoder=JSONEncoder)

def run_prices(request):
    Thread(target=get_prices).start()
    return JsonResponse({'success': True}, encoder=JSONEncoder)


@app.task
def get_prices():
    links = Link.objects.all()
    crawlers = {"iransote.com": iransote_com.iransote, "iranloop.ir": iranloop_ir.iranloop,
                "www.sazforoosh.com": www_sazforoosh_com.sazforoosh, "sazkala.com": sazkala_com.sazkala,
                "sedastore.com": sedastore_com.sedastore, "www.djcenter.net": www_djcenter_net.djcenter,
                "digiseda.ir": www_djcenter_net.djcenter, "rayanseda.com": rayanseda_com.rayanseda,
                "www.sornashop.com": www_sornashop_com.sornashop, "davarmelody.com": davarmelody_com.davarmelody,
                "www.tehranmelody.com": www_tehranmelody_com.tehranmelody,
                "tehranmelody.software": www_tehranmelody_com.tehranmelody,
                "navamarket.ir": navamarket_ir.navamarket, "golhastore.ir": golhastore_ir.golhastore,
                "ertebat.co": ertebat_co.ertebat, "delshadmusic.com": delshadmusic_com.delshadmusic,
                "delarammusic.com": delarammusic_com.delarammusic, "alikmusic.org": alikmusic_org.alikmusic,
                "violincenter.ir": violincenter_ir.violincenter, "donyayesazha.com": donyayesazha_com.donyayesazha,
                "sedabazar.com": sedabazar_com.sedabazar, "www.hezarsoo.com": www_hezarsoo_com.hezarsoo,
                "fluteshop.org": fluteshop_org.fluteshop, "digitalbaran.com": digitalbaran_com.digitalbaran,
                "turingsanat.com": turingsanat_com.turingsanat, "yerial.com": yerial_com.yerial,
                "www.gostaresh-seda.com": www_gostaresh_seda_com.gostaresh,
                "www.digikala.com": www_digikala_com.digikala,
                "www.sazplaza.com": www_sazplaza_com.sazplaza, "www.kalaoma.com": www_kalaoma_com.kalaoma,
                "jahanmelody.com": jahanmelody_com.jahanmelody, "echokowsar.com": echokowsar_com.echokowsar,
                "sotplus.ir": sotplus_ir.sotplus, "noornegar.com": noornegar_com.noornegar,
                "www.artemusic.ir": www_artemusic_ir.artemusic, "dgland.com": dgland_com.dgland,
                "saaz24.com": saaz24_com.saaz24, "melodinng.com": melodinng_com.melodinng,
                "www.afrangdigital.com": www_afrangdigital_com.afrangdigital,
                "parsiansote.com": parsiansote_com.parsiansote,
                "technicav.com": technicav_com.technicav, "www.didnegar.com": www_didnegar_com.didnegar,
                "www.alijavadzadeh.com": www_alijavadzadeh_com.alijavadzadeh, "bia2piano.ir": bia2piano_ir.bia2piano,
                "sedamoon.com": sedamoon_com.sedamoon, "malltina.com": malltina_com.malltina,
                "pishgaman-seda.com": pishgaman_seda_com.pishgaman, "www.dourbinet.com": www_dourbinet_com.dourbinet,
                "avatasvir.com": avatasvir_com.avatasvir, "hilatel.ir": hilatel_ir.hilatel,
                "www.yamahairan.ir": www_yamahairan_ir.yamahairan, "navakade.com": navakade_com.navakade,
                "head-phone.ir": head_phone_ir.head_phone, "touchmusic.ir": touchmusic_ir.touchmusic,
                "www.ghesticlub.com": www_ghesticlub_com.ghesticlub, "pcmaxhw.com": pcmaxhw_com.pcmaxhw,
                "www.pixel.ir": www_pixel_ir.pixel, "www.bokehland.com": www_bokehland_com.bokehland,
                "hajigame.ir": hajigame_ir.hajigame, "janebi.com": janebi_com.janebi,
                "jeddikala.com": jeddikala_com.jeddikala, "didbartarshop.ir": didbartarshop_ir.didbartarshop,
                "max-shop.ir": max_shop_ir.max_shop, "www.pakhsh.shop": www_pakhsh_shop.pakhsh,
                "www.safirkala.com": www_safirkala_com.safirkala, "namacam.ir": namacam_ir.namacam,
                "www.akasisaatchi.com": www_akasisaatchi_com.akasisaatchi, "www.flashiran.net": fluteshop_org.fluteshop,
                "mehragin.com": mehragin_com.mehragin, "barbadgallery.com": barbadgallery_com.barbadgallery,
                "zirpele.ir": zirpele_ir.zirpele, "parsacam.com": parsacam_com.parsacam,
                "negahshop.com": negahshop_com.negahshop, "didgahstore.ir": didgahstore_ir.didgahstore,
                "chavoosh110.com": chavoosh110_com.chavoosh110, "edbazar.com": edbazar_com.edbazar,
                "saz-bazar.com": saz_bazar_com.saz_bazar, "mahancamera.com": mahancamera_com.mahancamera,
                "avazac.com": avazac_com.avazac, "exif.ir": exif_ir.exif, "diddovom.com": diddovom_com.diddovom,
                "classicshopper.ir": classicshopper_ir.classicshopper, "golden8.ir": golden8_ir.golden8,
                "logilook.com": logilook_com.logilook, "lioncomputer.com": lioncomputer_com.lioncomputer,
                "bobloseven.com": bobloseven_com.bobloseven, "kingbrand.ir": kingbrand_ir.kingbrand,
                "jskala.com": jskala_com.jskala, "asarayan.com": asarayan_com.asarayan,
                "tehranspeaker.com": tehranspeaker_com.tehranspeaker, "technolife.ir": technolife_ir.technolife,
                "mahgoni.com": mahgoni_com.mahgoni, "zanbil.ir": zanbil_ir.zanbil, "gilsara.com": gilsara_com.gilsara,
                "esam.ir": esam_ir.esam, "bahartak.ir": bahartak_ir.bahartak, "mahor.net": mahor_net.mahor,
                "torob.com": torob_com.torob}
    # for link in links:
    import logging
    import datetime
    import time
    logger = logging.getLogger(__name__)
    config.lastCrawlStarted = datetime.datetime.now()
    config.lastCrawlChanges = 0

    for i in range(0, len(links)):
        time.sleep(0.5)
        link = links[i]
        site = re.findall("//(.*?)/", link.url)
        if not site:
            logger.info('empty url :  %s,', str(i))
            continue

        try:
            product = crawlers[site[0]](link, headers, site[0])
        except:
            logger.info('%s :  %s,', str(i), site[0])
            continue

        if product is None or product == 0:
            logger.info('null :  %s,', site[0])
            continue

        lastPrice = Price.objects.filter(parent=link).order_by('-created').first()
        if lastPrice is None or lastPrice.value != product:
            try:
                price = Price.objects.create(parent=link)
                price.value = product
                link.unseen = True
                musicItem = MusicItem.objects.get(pk=link.parent_id)
                if price.value == -1:
                    musicItem.out_of_stock += 1
                elif lastPrice is None or (lastPrice.value != -1 and lastPrice.value < price.value):
                    musicItem.increase += 1
                elif lastPrice.value == -1:
                    musicItem.in_stock += 1
                else:
                    musicItem.decrease += 1
                musicItem.save()
                price.save()
                link.save()
                config.lastCrawlChanges += 1
            except Exception as e:
                logger.info('%s', e)
    config.lastCrawlEnded = datetime.datetime.now()
    logger.info('done')
