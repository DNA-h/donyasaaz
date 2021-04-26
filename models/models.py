from django.db import models
from model_utils.models import TimeStampedModel
# Create your models here.

class MusicItem(TimeStampedModel):
    name = models.CharField(max_length=1024, null=True, blank=True)
    url = models.CharField(max_length=1024, null=True, blank=True)
    your_price = models.PositiveIntegerField(default=0, null=True, blank=True)
    image = models.CharField(max_length=1024, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
# create_update new Item(name,link,your_price,image)
# get list of items() => [item]
# delete item(id)

class Link(TimeStampedModel):
    url = models.CharField(max_length=1024, null=True, blank=True)
    parent = models.ForeignKey(MusicItem, null=True, blank=True, on_delete=models.CASCADE)
    unseen = models.BooleanField(default=False, null=True, blank=True)
# create_update new Link(url, parent_id)
# get list of links (parent_id) => [Link]
# delete  link (id)

class Price(TimeStampedModel):
    value = models.IntegerField(default=0, null=True, blank=True)
    parent = models.ForeignKey(Link, null=True, blank=True, on_delete=models.CASCADE)
# seen Link([id])
# upload image