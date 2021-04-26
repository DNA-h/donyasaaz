from django.shortcuts import render

# Create your views here.
from models.models import MusicItem, Link, Price
from rest_framework import serializers
from django.http import JsonResponse
from json import JSONEncoder
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes

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
            name=request.data["name"], url=request.data["url"],image=request.data["image"])
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
