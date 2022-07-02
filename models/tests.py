import re
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from json import JSONEncoder
from django.http import JsonResponse
from models.apis import crawlers

tests = [
    {"url": "https://digiseda.ir/153-rode-nt2-a.html?utm_medium=PPC&utm_source=Torob",
     "price": 12000000,
     "message": "digiseda_ir-1"},

    {"url": "https://www.ghestico.com/Installment/Product/988/Game-Console/Sony/Playstation-5-825GB-PS5",
     "price": 24400000,
     "message": "ghestico_com-1"},

    {"url": "https://www.ghestico.com/Installment/Product/1092/Mobile-Phone/Apple/TV-4K-32GB",
     "price": 5300000,
     "message": "ghestico_com-2"},

    {"url": "https://www.ghestico.com/Installment/Product/731/Mobile-Phone/Apple/iPhone-11-128GB-Dual-SIM",
     "price": -1,
     "message": "ghestico_com-3"},

    {"url": "https://m3sell.com/product/CineTracer",
     "price": 2300000,
     "message": "m3sell_com-1"},

    {"url": "https://m3sell.com/product/G-Preset-FullPack",
     "price": 110000,
     "message": "m3sell_com-2"},

    {"url": "https://m3sell.com/product/SoftBoxX5",
     "price": 1200000,
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
        "price": 26050000,
        "message": "santoorsadeghi-3"},

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
    # some issue with ul in price section

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
        "url": "https://www.khaneyesaaz.ir/%D8%B3%D8%A7%D8%B2%D9%87%D8%A7%DB%8C-%D8%AC%D9%87%D8%A7%D9%86%DB%8C/%D8%AA%D9%85%D9%BE%D9%88/%D8%AF%D8%A7%D8%B1%D8%A8%D9%88%DA%A9%D8%A7-%D8%AC%D9%88%D9%87%D8%B1%D8%A7%D9%84%D9%81%D9%86-%D9%85%D8%AF%D9%84-b22-6110?utm_medium=PPC&utm_source=Torob",
        "price": 11000000,
        "message": "khaneyesaaz.ir-1"
    },
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
        "url": "https://chavoosh110.com/product/%d9%85%db%8c%da%a9%d8%b1%d9%88%d9%81%d9%86-%d8%b4%d8%a7%d8%aa%da%af%d8%a7%d9%86-%d8%a8%d9%88%db%8c%d8%a7-boya-by-mm1/",
        "price": 780000,
        "message": "chavoosh110.com-1"
    },
    {
        "url": "https://chavoosh110.com/product/%D8%B1%DA%A9%D9%88%D8%B1%D8%AF%D8%B1-%D8%B5%D8%AF%D8%A7-zoom-h5/?utm_medium=PPC&utm_source=Torob",
        "price": 7600000,
        "message": "chavoosh110.com-2"
    },
    {
        "url": "https://chavoosh110.com/product/%D9%BE%D8%A7%DB%8C%D9%87-%D9%85%DB%8C%DA%A9%D8%B1%D9%88%D9%81%D9%86-%D8%A7%DB%8C%D8%B3%D8%AA%D8%A7%D8%AF%D9%87-%D9%87%D8%B1%DA%A9%D9%88%D9%84%D8%B3-hercules-ms531b/",
        "price": 2350000,
        "message": "chavoosh110.com-3"
    },
    # {
    #     "url": "https://www.mahdigit.ir/4k",
    #     "price": 999000,
    #     "message": "www.mahdigit.ir-1"
    # }, The price has no class in page web source
    # {
    #     "url": "https://www.mahdigit.ir/k8",
    #     "price": 348000,
    #     "message": "www.mahdigit.ir-2"
    # },
    # {
    #     "url": "https://www.mahdigit.ir/vitality-cross-action",
    #     "price": -1,
    #     "message": "www.mahdigit.ir-3"
    # },
    # {
    #     "url": "https://www.agrastore.ir/product/%da%a9%d9%86%d8%aa%d8%b1%d9%84%d8%b1-%d8%a7%d8%b3%d8%aa%d8%b1%db%8c%d9%85-%d8%a7%d9%84%da%af%d8%a7%d8%aa%d9%88-%d9%85%d8%af%d9%84-elgato-stream-deck-xl/",
    #     "price": 10428000,
    #     "message": "agrastore-1"
    # },
    # {
    #     "url": "https://www.agrastore.ir/product/%D9%85%DB%8C%DA%A9%D8%B1%D9%88%D9%81%D9%88%D9%86-saramonic-blink500-b4/?utm_medium=PPC&utm_source=Torob",
    #     "price": 8504000,
    #     "message": "agrastore-2"
    # },
    # {
    #     "url": "https://www.agrastore.ir/product/%D9%85%DB%8C%DA%A9%D8%B1%D9%88%D9%81%D9%86-%D8%AF%D8%A7%DB%8C%D9%86%D8%A7%D9%85%DB%8C%DA%A9-%D8%B4%D9%88%D8%B1-%D9%85%D8%AF%D9%84-sm7b/?utm_medium=PPC&utm_source=Torob",
    #     "price": -1,
    #     "message": "agrastore-3"
    # }, site is down
    {
        "url": "https://beethovenmshop.com/product/699/%D9%BE%DB%8C%D8%A7%D9%86%D9%88-%D8%AF%DB%8C%D8%AC%DB%8C%D8%AA%D8%A7%D9%84-%D8%A7%D8%B3%D8%AA%D9%88%D8%AF%DB%8C%D9%88-%D9%84%D8%A7%D8%AC%DB%8C%DA%A9-%D9%85%D8%AF%D9%84-numa-compact-2?utm_medium=PPC&utm_source=Torob",
        "price": 17500000,
        "message": "beethovenmshop-1"
    },
    {
        "url": "https://beethovenmshop.com/product/732/%D9%BE%DB%8C%D8%A7%D9%86%D9%88-%D8%AF%DB%8C%D8%AC%DB%8C%D8%AA%D8%A7%D9%84-%DB%8C%D8%A7%D9%85%D8%A7%D9%87%D8%A7-%D9%85%D8%AF%D9%84-clp-745",
        "price": 88500000,
        "message": "beethovenmshop-2"
    },
    {
        "url": "https://beethovenmshop.com/product/54/%D9%BE%DB%8C%D8%A7%D9%86%D9%88-%D8%AF%DB%8C%D8%AC%DB%8C%D8%AA%D8%A7%D9%84-%DB%8C%D8%A7%D9%85%D8%A7%D9%87%D8%A7-%D9%85%D8%AF%D9%84-p-125?utm_medium=PPC&utm_source=Torob",
        "price": -1,
        "message": "beethovenmshop-3"
    },
    {
        "url": "https://beethovenmshop.com/product/32/%DA%AF%DB%8C%D8%AA%D8%A7%D8%B1-%DA%A9%D9%84%D8%A7%D8%B3%DB%8C%DA%A9-%DB%8C%D8%A7%D9%85%D8%A7%D9%87%D8%A7-%D9%85%D8%AF%D9%84-cg122-mc",
        "price": -1,
        "message": "beethovenmshop-4"
    },
]

@csrf_exempt
@ api_view(['GET', 'POSt'])
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
