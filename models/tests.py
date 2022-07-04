import re
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from json import JSONEncoder
from django.http import JsonResponse
from models.apis import crawlers

tests = [
    # Todo don't check if it is too complicated
    # piece a cake ;-)
    # {
    #     "url": "https://sazzbazz.com/product/%D8%B3%D9%86%D8%AA%D9%88%D8%B1-%D8%B5%D8%A7%D8%AF%D9%82%DB%8C-%D9%82%D9%86%D8%A8%D8%B1%DB%8C-%D9%85%DB%8C%D9%86%DB%8C%D8%A7%D8%AA%D9%88%D8%B1/",
    #     "price": 9650000,
    #     "message": "sazzbazz.com-1"
    # },
    # some issue with ul in price section
    # Todo use regular expression
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
