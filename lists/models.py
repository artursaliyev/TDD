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


# class BoshBoshqarmaMarkaz(AbstractBoshqarma):
#     # yuridik adresi
#     viloyat = models.ForeignKey('Viloyat', related_name='boshboshqarmalar', on_delete=models.PROTECT)
#
#
#
# class Boshqarma(AbstractBoshqarma):
#     # yuridik adresi
#     viloyat = models.ForeignKey('Viloyat', related_name='boshqarmalar', on_delete=models.PROTECT)
#
#
#
# class Bolim(AbstractBoshqarma):
#     # yuridik adresi
#     tuman = models.ForeignKey('Tuman', related_name='bolimlar', on_delete=models.PROTECT)
#
