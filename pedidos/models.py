# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Inventory(models.Model):
    quantity = models.IntegerField(blank=True, null=True)
    product = models.ForeignKey('Product', models.DO_NOTHING)
    date = models.DateField(db_column='date', blank=True, null=True)

    class Meta:
        db_table = 'inventory'


class Product(models.Model):
    name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'product'


class Order(models.Model):
    priority = models.CharField(max_length=45, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING)
    delivery_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'order'


class OrderProducts(models.Model):
    product = models.ForeignKey(Product,  on_delete=models.CASCADE)
    order = models.ForeignKey(Order,  on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'order_products'


class Provider(models.Model):
    name = models.CharField(max_length=45, blank=True, null=True)
    products = models.ManyToManyField(Product)

    class Meta:
        db_table = 'provider'


class User(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'user'
