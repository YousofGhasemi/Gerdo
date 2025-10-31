import time

from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    default_currency = models.CharField(max_length=10, default="ریال")
    default_karat = models.PositiveSmallIntegerField(default=750)

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=50)
    debt = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.name


class Currency(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.code


class Commodity(models.Model):
    name = models.CharField(max_length=20)
    price = models.PositiveBigIntegerField()
    karat = models.PositiveSmallIntegerField(default=750)

    def __str__(self):
        return f"{self.name} : {self.karat}"


class Box(models.Model):
    name = models.CharField(max_length=50)
    data = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.name


class Bank(models.Model):
    name = models.CharField(max_length=50)
    cash = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f"{self.name}"


class Ledger(models.Model):
    user_created = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    date = models.DateTimeField(auto_now_add=True)
    is_debt = models.BooleanField()
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    exchange_currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    exchange_commodity = models.ForeignKey(
        Commodity,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    amount = models.PositiveIntegerField()
    price = models.PositiveIntegerField()

    @property
    def total(self):
        total = 0
        if self.exchange_commodity:
            total = self.amount * self.price
        else:
            total = (
                (self.exchange_commodity.karat / self.user_ctreated.default_karat)
                * self.amount
                * self.exchange_commodity.price
            )
        return total

    def clean_leger(self):
        if not self.exchange_currency and not self.exchange_commodity:
            raise ValidationError("یکی از فیلدهای ارز یا کالا باید پر شود")

        if self.exchange_currency and self.exchange_commodity:
            raise ValidationError("فقط یکی از فیلدهای ارز یا کالا می‌تواند پر شود")

    def __str__(self):
        name = (
            self.exchange_commodity
            if self.exchange_commodity
            else self.exchange_currency
        )
        unit = (
            self.exchange_commodity.unit
            if self.exchange_commodity
            else self.exchange_currency.code
        )
        return f"{self.date} - {"خرید" if self.is_debt else "فروش"} {name} - {self.amount} {unit}"

    class Meta:
        ordering = ["-date"]
