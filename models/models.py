from django.db import models
from model_utils.models import TimeStampedModel


# Create your models here.

class MusicItem(TimeStampedModel):
    class Meta:
        ordering = ['-decrease','-in_stock', '-increase','-out_of_stock']
    name = models.CharField(max_length=1024, null=True, blank=True)
    url = models.CharField(max_length=1024, null=True, blank=True)
    price = models.IntegerField(default=0, null=True, blank=True)
    image = models.CharField(max_length=1024, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    in_stock = models.SmallIntegerField(default=0, null=True, blank=True)
    out_of_stock = models.SmallIntegerField(default=0, null=True, blank=True)
    increase = models.SmallIntegerField(default=0, null=True, blank=True)
    decrease = models.SmallIntegerField(default=0, null=True, blank=True)


# create_update new Item(name,link,image)
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
