from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now

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
    last_modified = models.DateTimeField(blank=True)

    def update(self, force=False):
        if self.last_modified and (now() - self.last_modified).days == 0 and self.price and self.name and not force:
            return True

        res, title = skroutz.get_product_page(self.url)
        if res:
            self.name = title
            self.price = int(res[0]['price'])
            self.last_modified = now()
            return True
        else:
            return False

    def clean(self):
        if not self.update():
            raise ValidationError('Error')
        if not self.price:
            raise ValidationError('Error')

    def save(self, *args, **kwargs):
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


class Cooler(AbstractPart):
    pass


class Part(AbstractPart):
    description = models.CharField(max_length=32)
    pass
