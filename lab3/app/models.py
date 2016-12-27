from __future__ import unicode_literals

from django.db import models


class Stock(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    capacity = models.IntegerField()


class Product(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    cost = models.FloatField()
    amount = models.IntegerField()
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    data_time = models.DateTimeField()
    amount = models.IntegerField()

