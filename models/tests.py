import re
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from json import JSONEncoder
from django.http import JsonResponse
from models.apis import crawlers

tests = [
    {
        "url": "https://www.zhovanmusic.com/store/sell-musical-instruments/piano-sales/yamaha-ydp-145",
        "price": 49200000, "message": "zhovanmusic-1"
    }, {
        "url": "https://www.zhovanmusic.com/store/sell-musical-instruments/piano-sales/yamaha-clp-725?utm_medium=PPC&utm_source=Torob",
        "price": 63500000, "message": "zhovanmusic-2"
    }, {
        "url": "https://www.zhovanmusic.com/store/sell-musical-instruments/piano-sales/yamaha-ydp-144?utm_medium=PPC&utm_source=Torob",
        "price": 42000000, "message": "zhovanmusic-3"
    }, {
        "url": "https://sinacamera.ir/Product/BKP-20185/%d8%af%d8%b3%d8%aa%da%af%d8%a7%d9%87-%d8%a7%d8%b5%d9%84%d8%a7%d8%ad-%d8%b1%d9%86%da%af-%d9%88-%da%a9%d8%a7%d9%84%db%8c%d8%a8%d8%b1%d9%87-%d9%85%d8%a7%d9%86%db%8c%d8%aa%d9%88%d8%b1-x-rite-i1display-stu/",
        "price": 6800000, "message": "sinacamera-1"
    }, {
        "url": "https://sinacamera.ir/Product/BKP-19735/%d8%af%d9%88%d8%b1%d8%a8%db%8c%d9%86-%d8%a8%d8%af%d9%88%d9%86-%d8%a2%db%8c%d9%86%d9%87-%da%a9%d8%a7%d9%86%d9%86-canon-eos-m50-mark-ii-kit-15-45mm-f-3-5-6-3-is-stm/",
        "price": 19800000, "message": "sinacamera-2"
    }, {
        "url": "https://sinacamera.ir/Product/BKP-20071/%d8%af%d9%88%d8%b1%d8%a8%db%8c%d9%86-%d8%a8%d8%af%d9%88%d9%86-%d8%a2%db%8c%d9%86%d9%87-%da%a9%d8%a7%d9%86%d9%86-canon-eos-rp-mount-adapter-ef-eos-r-ef-24-105mm-canon-eos-rp/",
        "price": -1, "message": "sinacamera-3"
    }, {
        "url": "https://turborayan.com/%D8%A7%D8%B3%D9%BE%DB%8C%DA%A9%D8%B1-speaker/19841-%D8%A7%D8%B3%D9%BE%DB%8C%DA%A9%D8%B1-%D8%AF%D9%88-%D8%AA%DB%8C%DA%A9%D9%87-%D8%AA%D8%B3%DA%A9%D9%88-tsco-2066.html",
        "price": 284000, "message": "turborayan-1"
    }, {
        "url": "https://turborayan.com/%D9%BE%D8%A7%DB%8C%D9%87-%D8%AF%DB%8C%D9%88%D8%A7%D8%B1%DB%8C-%D8%B1%D9%88%D9%85%DB%8C%D8%B2%DB%8C-%D9%85%D8%A7%D9%86%DB%8C%D8%AA%D9%88%D8%B1/28076-%D9%BE%D8%A7%D9%8A%D9%87-%D9%86%DA%AF%D9%87%D8%AF%D8%A7%D8%B1%D9%86%D8%AF%D9%87-%D9%84%D9%BE-%D8%AA%D8%A7%D9%BE-%D8%AC%D9%8A%D8%A8%DB%8C-wlb003.html",
        "price": 625000, "message": "turborayan-2"
    }, {
        "url": "https://turborayan.com/%D9%81%DB%8C%D8%B4-%D9%BE%D8%B1%DB%8C%D9%86%D8%AA%D8%B1/14809-%D9%81%DB%8C%D8%B4-%D9%BE%D8%B1%DB%8C%D9%86%D8%AA%D8%B1-tp1000-%D9%85%DB%8C%D9%88%D8%A7.html",
        "price": 2700000, "message": "turborayan-3"
    },
    {"url": "https://www.ghestico.com/Installment/Product/988/Game-Console/Sony/Playstation-5-825GB-PS5",
     "price": 24400000,
     "message": "ghestico_com-1"},

    {"url": "https://www.ghestico.com/Installment/Product/1092/Mobile-Phone/Apple/TV-4K-32GB",
     "price": 5300000,
     "message": "ghestico_com-2"},

    {"url": "https://www.ghestico.com/Installment/Product/731/Mobile-Phone/Apple/iPhone-11-128GB-Dual-SIM",
     "price": -1,
     "message": "ghestico_com-3"},

    {"url": "https://zhiyunkala.com/product/crane-2s/",
     "price": 17250000,
     "message": "zhiyunkala_com-1"},

    {"url": "https://zhiyunkala.com/product/by-k2/",
     "price": 630000,
     "message": "zhiyunkala_com-2"},

    {"url": "https://zhiyunkala.com/product/dell-vostro-5470/",
     "price": -1,
     "message": "zhiyunkala_com-3"},

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
        "url": "https://santoorsadeghi.ir/product/%d8%b3%d9%86%d8%aa%d9%88%d8%b1-%d8%b5%d8%a7%d8%af%d9%82%db%8c-%d8%a2%d9%88%d8%a7%db%8c-%d8%b9%d8%b4%d9%82-%d8%b7%d8%b1%d8%ad-%d9%86%d9%82%d8%a7%d8%b4%db%8c/",
        "price": 50000000,
        "message": "santoorsadeghi-1"},#two santoorsadeghi crawler name in apis maybe it's the reason why it doesn't work

    {
        "url": "https://santoorsadeghi.ir/product/%d8%b3%d9%86%d8%aa%d9%88%d8%b1-%d8%b5%d8%a7%d8%af%d9%82%db%8c-%d8%aa%da%a9-%d9%85%d9%87%d8%b1/",
        "price": 3300000,
        "message": "santoorsadeghi-2"},

    {
        "url": "https://santoorsadeghi.ir/product/%d8%b3%d9%86%d8%aa%d9%88%d8%b1-%d8%b5%d8%a7%d8%af%d9%82%db%8c-%d8%b3%d9%81%d8%a7%d8%b1%d8%b4%db%8c/",
        "price": -1,
        "message": "santoorsadeghi-3"},

    {
        "url": "https://canon1.ir/%D9%85%D8%AD%D8%B5%D9%88%D9%84%D8%A7%D8%AA/%d9%85%d8%b9%d8%b1%d9%81%db%8c-%d9%88-%d8%a8%d8%b1%d8%b1%d8%b3%db%8c-%d9%84%d9%86%d8%b2-canon-ef-s-18-135mm-f3-5-5-6-is/",
        "price": 12300000,
        "message": "canon1_ir-1"},

    {
        "url": "https://canon1.ir/%D9%85%D8%AD%D8%B5%D9%88%D9%84%D8%A7%D8%AA/%d8%af%d9%88%d8%b1%d8%a8%db%8c%d9%86-%da%a9%d8%a7%d9%86%d9%86-canon-m50-18-150mm/",
        "price": 29700000,
        "message": "canon1_ir-2"},

    {
        "url": "https://canon1.ir/%D9%85%D8%AD%D8%B5%D9%88%D9%84%D8%A7%D8%AA/%D8%AF%D9%88%D8%B1%D8%A8%DB%8C%D9%86-canon-eos-760d/",
        "price": -1,
        "message": "canon1_ir-3"},

    {
        "url": "https://memorybazar.com/product/%d8%a7%d9%86%d8%af%d8%b1%d9%88%db%8c%d8%af-%d8%a8%d8%a7%da%a9%d8%b3-%d9%85%d8%af%d9%84-a95x-f4-4-64/",
        "price": 2179000,
        "message": "memorybazar-1"},

    {
        "url": "https://memorybazar.com/product/%da%af%db%8c%d9%85%d8%a8%d8%a7%d9%84-%da%98%db%8c%d9%88%d9%86-%d9%85%d8%af%d9%84-smooth-q2/",
        "price": 2200000,
        "message": "memorybazar-2"},

    {"url": "https://memorybazar.com/product/android-box-keyboard-c120/",
     "price": -1,
     "message": "memorybazar-3"},

    # {"url": "https://www.rayanmusic.com/cort-x100-opbb",#thi site has issue with ul in price
    #  "price": 6880000,
    #  "message": "rayanmusic_com-1"},
    #
    # {"url": "https://www.rayanmusic.com/ibanez-rgr652ahbf-wk",
    #  "price": 68400000,
    #  "message": "rayanmusic_com-2"},
    #
    # {"url": "https://www.rayanmusic.com/cort-x100-opbk",
    #  "price": 0,
    #  "message": "rayanmusic_com-3"},

    {"url": "https://nobesho.com/product/nbp-5741236098",
     "price": 290000,
     "message": "nobesho_com-1"},

    {"url": "https://nobesho.com/product/nbs-27615348",
     "price": 49000,
     "message": "nobesho_com-2"},

    {"url": "https://nobesho.com/product/nbs-05138794",
     "price": -1,
     "message": "nobesho_com-3"},

    {"url": "https://1xmarket.com/product/rapoo-gk500punk-mechanical-gaming-keyboard/",
     "price": 1710000,
     "message": "www_1xmarket_com-1"},

    {"url": "https://1xmarket.com/product/rapoo-gk500punk-mechanical-gaming-keyboard/",
     "price": 1710000,
     "message": "www_1xmarket_com-2"},

    {"url": "https://1xmarket.com/product/ssd-hard-lexar-nm610-1tb-internal/",
     "price": -1,
     "message": "www_1xmarket_com-3"},

    {
        "url": "https://nooracam.com/product/%d8%b1%db%8c%d9%86%da%af-%d9%84%d8%a7%db%8c%d8%aa-ring-light-yq-320a-32w-%d9%be%d8%a7%db%8c%d9%87/",
        "price": 600000,
        "message": "nooracam_com-1"},

    {
        "url": "https://nooracam.com/product/%d8%af%d9%88%d8%b1%d8%a8%db%8c%d9%86-%d8%b9%da%a9%d8%a7%d8%b3%db%8c-%d9%86%db%8c%da%a9%d9%88%d9%86-nikon-d780-body/",
        "price": 55500000,
        "message": "nooracam_com-2"},

    {
        "url": "https://nooracam.com/product/%d8%af%d9%88%d8%b1%d8%a8%db%8c%d9%86-%d8%a8%d8%af%d9%88%d9%86-%d8%a2%db%8c%d9%86%d9%87-%d8%b3%d9%88%d9%86%db%8c-sony-alpha-a6400-body/",
        "price": 43500000,
        "message": "nooracam_com-3"},

    {
        "url": "https://nooracam.com/product/%d8%af%d9%88%d8%b1%d8%a8%db%8c%d9%86-%d8%b9%da%a9%d8%a7%d8%b3%db%8c-%da%a9%d8%a7%d9%86%d9%86-canon-eos-90d-dslr-kit-18-55mm-stm/",
        "price": 37100000,
        "message": "nooracam_com-4"},
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
            print("++",test['message'])
        else:
            print("--",test['message'], product)
    return JsonResponse({'success': True}, encoder=JSONEncoder)
