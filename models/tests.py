import re
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from json import JSONEncoder
from django.http import JsonResponse
from models.apis import crawlers

tests = [
    {"url": "https://m3sell.com/product/CineTracer",
     "price": 2300000,
     "message": "m3sell_com-1"},

    {"url": "https://m3sell.com/product/G-Preset-FullPack",
     "price": 110000,
     "message": "m3sell_com-2"},

    {"url": "https://m3sell.com/product/SoftBoxX5",
     "price": 1300000,
     "message": "m3sell_com-3"},

    {
        "url": "http://sazplus.com/product/%da%a9%d8%a7%d8%ae%d9%86-%d8%b3%d9%84%d8%a7-se-012/",
        "price": 8200000,
        "message": "sazplus.com-1"
    },

    {
        "url": "http://sazplus.com/product/%d9%88%db%8c%d9%88%d9%84%d9%86-%d9%85%d9%88%d9%84%d8%b1-%d9%85%d8%af%d9%84-500-%d8%b3%d8%a7%db%8c%d8%b2-3-4/",
        "price": 5800000,
        "message": "sazplus.com-2"
    },

    {
        "url": "http://sazplus.com/product/%d9%88%db%8c%d9%88%d9%84%d9%86-%d8%a2%d9%85%d8%a7%d8%aa%db%8c-%d9%85%d8%af%d9%84-100-%d8%b3%d8%a7%db%8c%d8%b2-2-4/?utm_medium=PPC",
        "price": 2850000,
        "message": "sazplus.com-3"
    },

    {
        "url": "https://saazaar.com/product/%da%a9%db%8c%d9%85%d9%86%d8%af-%d9%85%d8%ac%d8%b0%d9%88%d8%a8/",
        "price": 14040000,
        "message": "saazaar.com-1"
    },

    {
        "url": "https://saazaar.com/product/%d8%b3%db%8c%d9%85-%da%a9%d9%85%d8%a7%d9%86%da%86%d9%87-%d8%a7%d8%b3%d8%aa%d8%b1%db%8c%d9%86%da%af%d8%b1-%d8%b3%db%8c%d9%84%d9%88%d8%b1/",
        "price": 650000,
        "message": "saazaar.com-2"
    },

    {
        "url": "https://saazaar.com/product/%d9%be%d8%b1%d8%af%d9%87-%d8%b3%d9%87-%d8%aa%d8%a7%d8%b1-%d9%be%d9%84%db%8c%d9%85%d8%b1%db%8c/",
        "price": -1,
        "message": "saazaar.com-3"
    },

    {
        "url": "https://sazzbazz.com/product/%D8%B3%D9%86%D8%AA%D9%88%D8%B1-%D8%B5%D8%A7%D8%AF%D9%82%DB%8C-%D9%82%D9%86%D8%A8%D8%B1%DB%8C-%D9%85%DB%8C%D9%86%DB%8C%D8%A7%D8%AA%D9%88%D8%B1/",
        "price": 9185000,
        "message": "sazzbazz.com-1"
    },

    {
        "url": "https://basalam.com/payam-art/product/3063673?utm_medium=PPC&utm_source=Torob",
        "price": 2049000,
        "message": "basalam.com-1"
    },

    # {"url": "https://www.rayanmusic.com/cort-x100-opbb",#thi site has issue with ul in price
    #  "price": 8250000,
    #  "message": "rayanmusic_com-1"},
    #
    # {"url": "https://www.rayanmusic.com/ibanez-rgr652ahbf-wk",
    #  "price": 75390000,
    #  "message": "rayanmusic_com-2"},
    #
    # {"url": "https://www.rayanmusic.com/cort-x100-opbk",
    #  "price": 0,
    #  "message": "rayanmusic_com-3"},

    {
        "url": "https://www.khaneyesaaz.ir/%D8%B3%D8%A7%D8%B2%D9%87%D8%A7%DB%8C-%D8%AC%D9%87%D8%A7%D9%86%DB%8C/%D8%AA%D9%85%D9%BE%D9%88/%D8%AF%D8%A7%D8%B1%D8%A8%D9%88%DA%A9%D8%A7-%D8%AC%D9%88%D9%87%D8%B1%D8%A7%D9%84%D9%81%D9%86-%D9%85%D8%AF%D9%84-b22-6110?utm_medium=PPC&utm_source=Torob",
        "price": 11000000,
        "message": "khaneyesaaz.ir-1"
    },
    # crawlers is ok and run correctly but doesn't work in test
    {
        "url": "https://www.khaneyesaaz.ir/%D8%B3%D8%A7%D8%B2-%D8%A7%DB%8C%D8%B1%D8%A7%D9%86%DB%8C/%D8%A8%D8%A7%D8%BA%D9%84%D8%A7%D9%85%D8%A7/%D8%A8%D8%A7%D8%BA%D9%84%D8%A7%D9%85%D8%A7-%D8%AF%D8%B3%D8%AA%D9%87-%D8%A8%D9%84%D9%86%D8%AF-%D9%87%D9%86%D8%A7%D8%B1%D9%87?utm_medium=PPC&utm_source=Torob",
        "price": 2950000,
        "message": "khaneyesaaz.ir-2"
    },
    {
        "url": "https://www.khaneyesaaz.ir/%D8%B3%D8%A7%D8%B2%D9%87%D8%A7%DB%8C-%D8%AC%D9%87%D8%A7%D9%86%DB%8C/%DA%AF%DB%8C%D8%AA%D8%A7%D8%B1/%D9%BE%DA%A9%DB%8C%D8%AC-%DA%AF%DB%8C%D8%AA%D8%A7%D8%B1-%D8%A7%D9%84%DA%A9%D8%AA%D8%B1%DB%8C%DA%A9-%DB%8C%D8%A7%D9%85%D8%A7%D9%87%D8%A7-%D9%85%D8%AF%D9%84-erg121gp?utm_medium=PPC&utm_source=Torob",
        "price": 9750000,
        "message": "khaneyesaaz.ir-3"
    },
    {
        "url": "https://www.mahdigit.ir/4k",
        "price": 1200000,
        "message": "www.mahdigit.ir-1"
    },
    {
        "url": "https://www.mahdigit.ir/k8",
        "price": 348000,
        "message": "www.mahdigit.ir-2"
    },
    {
        "url": "https://www.mahdigit.ir/vitality-cross-action",
        "price": -1,
        "message": "www.mahdigit.ir-3"
    },
    {
        "url": "https://www.khaneyesaaz.ir/%D8%B3%D8%A7%D8%B2%D9%87%D8%A7%DB%8C-%D8%AC%D9%87%D8%A7%D9%86%DB%8C/%D9%87%D9%86%DA%AF-%D8%AF%D8%B1%D8%A7%D9%85/%D9%87%D9%86%DA%AF%D8%AF%D8%B1%D8%A7%D9%85-9%D9%86%D8%AA-%DA%A9%DB%8C%D8%AA%D8%A7-%D9%BE%D9%86%D8%AA%D8%A7%D9%85?utm_medium=PPC&utm_source=Torob",
        "price": 16000000,
        "message": "reported-3"
    },
    {
        "url": "https://www.khaneyesaaz.ir/%D9%84%D9%88%D8%A7%D8%B2%D9%85-%D8%AC%D8%A7%D9%86%D8%A8%DB%8C/%D8%B3%D8%A7%D8%B2%D9%87%D8%A7%DB%8C-%D8%A2%D8%B1%D8%B4%D9%87-%D8%A7%DB%8C/%D9%84%D9%88%D8%A7%D8%B2%D9%85-%D8%AC%D8%A7%D9%86%D8%A8%DB%8C-%D9%88%DB%8C%D9%88%D9%84%D9%86/%D8%B3%DB%8C%D9%85-%D9%88%DB%8C%D9%88%D9%84%D9%86-%D9%BE%DB%8C%D8%B1%D8%A7%D8%B3%D8%AA%D8%B1%D9%88-%D8%B3%D8%A8%D8%B2-%D9%85%D8%AF%D9%84-chromcor?utm_medium=PPC&utm_source=Torob",
        "price": 1300000,
        "message": "reported-4"
    },
    {
        "url": "https://www.sazbebar.com/shop/guitar/electric-guitars/%D9%BE%DA%A9%DB%8C%D8%AC-%DA%AF%DB%8C%D8%AA%D8%A7%D8%B1-%D8%A7%D9%84%DA%A9%D8%AA%D8%B1%DB%8C%DA%A9-%DB%8C%D8%A7%D9%85%D8%A7%D9%87%D8%A7-%D9%85%D8%AF%D9%84-eg112c/?utm_medium=PPC&utm_source=Torob",
        "price": 10200000,
        "message": "sazbebar-1"
    },
    {
        "url": "https://www.sazbebar.com/shop/wind-instruments/trumpet/%D8%AA%D8%B1%D9%88%D9%85%D9%BE%D8%AA-%DB%8C%D8%A7%D9%85%D8%A7%D9%87%D8%A7-%D9%85%D8%AF%D9%84-ytr-2330/",
        "price": 2620000,
        "message": "sazbebar-2"
    },
    {
        "url": "https://www.sazbebar.com/shop/guitar/acoustic-guitars/%da%af%db%8c%d8%aa%d8%a7%d8%b1-%d8%a2%da%a9%d9%88%d8%b3%d8%aa%db%8c%da%a9-%d8%a2%d9%86%d8%af%d8%b1%d8%b3-f-4140-c/",
        "price": -1,
        "message": "sazbebar-3"
    },
    {
        "url": "https://dragon-shop.ir/product/%d9%be%d8%af-%d8%b5%d9%86%d8%af%d9%84%db%8c-%da%af%db%8c%d9%85%db%8c%d9%86%da%af-%d9%81%d9%84%d9%88%d8%b1%d9%be%d8%af-%d8%b7%d8%b1%d8%ad-florpad-arctic/",
        "price": -1,
        "message": "dragon-shop-1"
    },
]


@csrf_exempt
@api_view(['GET', 'POSt'])
def run_tests(request):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}

    class Object(object):
        pass

    a = Object()

    for test in tests:
        site = re.findall("//(.*?)/", test['url'])
        a.url = test['url']
        product = crawlers[site[0]](a, headers, site[0])
        if product == test['price']:
            print("++", test['message'])
        else:
            print("--", test['message'], product)
    return JsonResponse({'success': True}, encoder=JSONEncoder)
