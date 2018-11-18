# coding: utf-8
from __future__ import unicode_literals
import datetime

from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils import timezone


# Create your models here.

class BaseModel(models.Model):
    create_time = models.DateTimeField(default=timezone.now)
    modify_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Company(BaseModel):
    name = models.CharField(max_length=64)
    slug = models.CharField(unique=True)

    def __unicode__(self):
        return self.name


class Agent(BaseModel):
    name = models.CharField(max_length=64)
    belong = models.ForeignKey(Company, related_name='company_agents')


class Store(BaseModel):
    store_type_choices = [
        (1, '汽服终端'),
        (2, '加油站'),
    ]
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
    store_type = models.IntegerField(default=1, choices=store_type_choices)
    belong = models.ForeignKey(Agent, related_name='agent_stores', null=True, blank=True)
    parent_belong = models.ForeignKey(Company, related_name='company_gas_stations', null=True, blank=True)

    def __unicode__(self):
        return self.name


class CloudUser(AbstractBaseUser):
    user_type_choices = [
        (0, '公司人员'),
        (1, '经销商'),
        (2, '汽服终端'),
    ]
    role_choices = [
        (0, '销售代表'),
        (1, '区域经理'),
        (2, '物流岗'),
        (3, '价格审计'),
        (4, '超级管理员'),
    ]
    name = models.CharField(max_length=64)
    user_type = models.IntegerField(default=0, choices=user_type_choices)
    role = models.IntegerField(default=0, choices=role_choices)
    company_belong = models.ForeignKey(Company, related_name='company_users', null=True, blank=True)
    agent_belong = models.ForeignKey(Agent, related_name='agent_users', null=True, blank=True)
    store_belong = models.ForeignKey(Store, related_name='store_users', null=True, blank=True)

    def __unicode__(self):
        return self.name


class Warehouse(BaseModel):
    house_type_choices = [
        (1, '汽服终端仓库'),
        (2, '经销商仓库'),
        (3, '公司仓库'),
    ]

    name = models.CharField(max_length=64)
    address = models.CharField(max_length=200, default='', null=True, blank=True)
    lat = models.FloatField(default=0)
    lon = models.FloatField(default=0)
    province = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    house_type = models.IntegerField(default=1, choices=house_type_choices)
    store_belong = models.ForeignKey(Store, related_name='store_warehouses', null=True, blank=True)
    agent_belong = models.ForeignKey(Store, related_name='agent_warehouses', null=True, blank=True)
    company_belong = models.ForeignKey(Store, related_name='company_warehouses', null=True, blank=True)

    def __unicode__(self):
        return self.name


class Classification(BaseModel):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name


class Good(BaseModel):
    name = models.CharField(max_length=64)
    till_code = models.CharField(max_length=64)
    description = models.CharField(max_length=128, null=True, blank=True)
    picture = models.CharField(max_length=128, null=True, blank=True, default='')
    unit = models.CharField(max_length=10, null=True, blank=True, default='桶')
    classification = models.ForeignKey(Classification, related_name='cls_goods', null=True, blank=True)
    price = models.FloatField(default=0.0)

    def __unicode__(self):
        return self.name


class Inventory(BaseModel):
    '''
    库存
    '''
    item = models.ForeignKey(Good, related_name='goods_ints')
    belong = models.ForeignKey(Warehouse, related_name='warehouse_ints')

    current_nums = models.IntegerField(default=0)
    max_nums = models.IntegerField(default=0)
    min_nums = models.IntegerField(default=100)

    def __unicode__(self):
        return '{0}-{1}: {2}{3}'.format(self.belong.name, self.item.name, self.current_nums, self.item.unit)


class Order(BaseModel):
    '''
    订单
    '''

    order_type_choices = [
        (0, '汽服订单'),
        (1, '经销商订单'),
    ]
    status_choices = [
        (0, '待审核'),
        (1, '销售代表确认'),
        (2, '区域经理确认'),
        (3, '物流确认'),
        (4, '价格审核中'),
        (5, '待发货'),
        (6, '配送中'),
        (7, '已完成'),
    ]
    order_id = models.CharField(max_length=128, unique=True)
    status = models.IntegerField(default=0, choices=status_choices)
    address = models.CharField(max_length=256, default='')
    # deliver = models.ForeignKey()
    seller = models.CharField(max_length=128, default='')
    seller_address = models.CharField(max_length=128, default='')
    total_price = models.FloatField(default=0.0)
    last_price = models.FloatField(default=0.0)
    order_type = models.IntegerField(default=0, choices=order_type_choices)
    store_belong = models.ForeignKey(Store, related_name='store_orders', null=True, blank=True)
    agent_belong = models.ForeignKey(Agent, related_name='agent_orders', null=True, blank=True)
    create_by = models.ForeignKey(CloudUser, related_name='user_orders')

    def __unicode__(self):
        if not self.order_type:
            return '{0}-{1}'.format(self.store_belong.name, self.order_id)
        return '{0}-{1}'.format(self.agent_belong.name, self.order_id)


class OrderItem(BaseModel):
    '''
    订单详情
    '''
    item = models.ForeignKey(Good, related_name='good_items')
    numbers = models.IntegerField(default=0)
    total_price = models.FloatField(default=0.0)
    belong = models.ForeignKey(Order, related_name='order_details')

    def __unicode__(self):
        return '{3}: {0}x{1} {2}'.format(self.item.name, self.numbers, self.total_price, self.belong.order_id)


class StorageOrder(BaseModel):
    '''
    入库单
    '''

    storage_id = models.CharField(max_length=128, unique=True)
    item = models.ForeignKey(Good, related_name='good_storage_items')
    numbers = models.IntegerField(default=0)
    # 入库价格
    price = models.FloatField(default=0.0)
    belong = models.ForeignKey(Warehouse, related_name='warehouse_storage_orders')
    create_by = models.ForeignKey(CloudUser, related_name='user_storage_orders')

    def __unicode__(self):
        return self.storage_id
