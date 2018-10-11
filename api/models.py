# coding: utf-8
from __future__ import unicode_literals
import datetime
from django.db import models
from django.utils import timezone


# Create your models here.

class BaseModel(models.Model):
    create_time = models.DateTimeField(default=timezone.now)
    modify_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Store(BaseModel):
    name = models.CharField(max_length=40)
    picture = models.CharField(max_length=128, default='/static/img/default.jpg')
    phone = models.CharField(max_length=20, default='', null=True, blank=True)
    score = models.FloatField(default=5.0)
    province = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    address = models.CharField(max_length=200, default='', null=True, blank=True)
    inventory = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    lat = models.FloatField(default=0)
    lon = models.FloatField(default=0)

    def __unicode__(self):
        return self.name
