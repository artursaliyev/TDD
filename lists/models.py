from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # region = models.ForeignKey('Region', on_delete=models.PROTECT)
    pass


class AbstractBoshqarma(models.Model):
    nomi_tashqi = models.CharField(max_length=50)
    nomi_ichki = models.CharField(max_length=50)
    xodimlar_soni = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True


class Item(models.Model):
    text = models.TextField()
    list = models.ForeignKey('List', on_delete=models.CASCADE, default=None)


class List(models.Model):
    pass

