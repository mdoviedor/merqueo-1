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

    class Meta:
        managed = False
        db_table = 'inventory'


class Order(models.Model):
    priority = models.CharField(max_length=45, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING)
    deliverydate = models.DateField(db_column='deliveryDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'order'


class OrderHasProduct(models.Model):
    order = models.ForeignKey(Order, models.DO_NOTHING, primary_key=True)
    product = models.ForeignKey('Product', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'order_has_product'
        unique_together = (('order', 'product'),)


class Product(models.Model):
    name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product'


class Provider(models.Model):
    name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'provider'


class ProviderHasProduct(models.Model):
    provider = models.ForeignKey(Provider, models.DO_NOTHING, primary_key=True)
    product = models.ForeignKey(Product, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'provider_has_product'
        unique_together = (('provider', 'product'),)


class User(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'
