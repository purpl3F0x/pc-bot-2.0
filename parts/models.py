from django.core.exceptions import ValidationError
from django.db import models

import skroutz_scrapper as skroutz


# Validators

def validate_skroutz_url(url):
    if "skroutz.gr/" not in url:
        raise ValidationError("Not Skroutz url")


# Choices
PSU_80P_CHOICES = (
    (('-',) * 2),
    (('80 PLUS',) * 2),
    (('80 PLUS Bronze',) * 2),
    (('80 PLUS Silver',) * 2),
    (('80 PLUS Gold',) * 2),
    (('80 PLUS Platinum',) * 2),
    (('80 PLUS Titanium',) * 2),
)


# Create your models here.

class AbstractPart(models.Model):
    url = models.URLField(unique=True, blank=False, validators=[validate_skroutz_url])
    name = models.CharField(blank=True, max_length=128)
    price = models.IntegerField(blank=True)

    def clean(self):
        if not self.name or not self.price:
            raise ValidationError('Seems there was a problem, Check url is valid else try later')

    def save(self, *args, **kwargs):
        try:
            res, title = skroutz.get_product_page(self.url)
            if len(res):
                self.name = title if not self.name else self.name
                self.price = int(res[0]['price'])

        finally:
            self.full_clean()
            super(AbstractPart, self).save(*args, **kwargs)

    def publish(self):
        self.save()

    def __str__(self):
        return self.name if self.name else self.url

    class Meta:
        abstract = True


class CPU(AbstractPart):
    pass


class Motherboard(AbstractPart):
    pass


class RAM(AbstractPart):
    pass


class GPU(AbstractPart):
    pass


class PSU(AbstractPart):
    pass


class Case(AbstractPart):
    pass


class Part(AbstractPart):
    pass


class Entity(models.Model):
    cpu = models.ForeignKey(CPU, blank=False, on_delete=models.PROTECT)
    ram = models.ForeignKey(RAM, blank=False, on_delete=models.PROTECT)
    motherboard = models.ForeignKey(Motherboard, blank=False, null=True, on_delete=models.PROTECT)
    psu = models.ForeignKey(PSU, blank=False, on_delete=models.PROTECT)
    gpu = models.ForeignKey(GPU, blank=True, null=True, on_delete=models.PROTECT)

    case = models.ManyToManyField(Case, blank=True)

    rest_items = models.ManyToManyField(Part, blank=True)
