from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
class UserProfile(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, primary_key=True
    )
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=48)

    def __str__(self):
        return self.name


class Customers(models.Model):
    name = models.CharField(max_length=50)
    debt = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.name


class Currency(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    decimal_point = models.DecimalField(
        max_digits=11,
        decimal_places=2,
    )

    def __str__(self):
        return self.code


class Box(models.Model):
    name = models.CharField(max_length=50)
    data = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.name
