from random import choice

from discord import Colour, Embed
from django.core.validators import RegexValidator
from django.db import models

import lists.common as common


class Tag(models.Model):
    val = models.CharField(max_length=15)

    def publish(self):
        self.save()

    def __str__(self):
        return self.val


class Pc(models.Model):
    price = models.IntegerField(blank=False)

    # Specs
    cpu = models.CharField(max_length=64, blank=False)
    gpu = models.CharField(max_length=64, blank=True)
    mobo = models.CharField(max_length=64, blank=False)
    ram = models.CharField(max_length=64, blank=False)
    psu = models.CharField(max_length=64, blank=False)
    ssd = models.CharField(max_length=64, blank=True)
    hdd = models.CharField(max_length=64, blank=True)
    cooler = models.CharField(max_length=64, blank=True)
    case = models.CharField(max_length=64, blank=True)

    active = models.BooleanField(default=True)

    tags = models.ManyToManyField(Tag)

    comment = models.TextField(blank=True)

    def publish(self):
        self.save()

    def __str__(self):
        return str(self.price) + '€ (' + self.cpu + ')'

    def getSpecs(self):  # Oh this is going to be a messsh!
        out = ''
        out += 'CPU: ' + self.cpu + '\n'

        if self.gpu:
            out += 'GPU: ' + self.gpu + '\n'

        out += 'Mobo: ' + self.mobo + '\n'
        out += 'RAM: ' + self.ram + '\n'
        out += 'PSU: ' + self.psu + '\n'

        if self.ssd:
            out += 'SSD: ' + self.ssd + '\n'
        if self.hdd:
            out += 'HDD: ' + self.hdd + '\n'
        if self.case:
            out += 'Case: ' + self.case + '\n'
        if self.cooler:
            out += 'Cooler: ' + self.cooler + '\n'

        return out

    def getemded(self):

        embed = Embed(title=str(self.price) + "€", colour=Colour(0x8567ff), url="http://3.120.5.250:8000/",
                      description="*" + choice(common.captions) + ".*")

        # embed.set_image(url="https://media.giphy.com/media/aFfYlsEdiWPDi/giphy.gif")
        embed.set_thumbnail(url="https://s3.amazonaws.com/gs-geo-images/356c3dd8-5d59-48cd-9a0b-5d638e6d48cd.gif")
        embed.set_author(name="Hal", url="http://3.120.5.250:8000/",
                         icon_url="https://media.giphy.com/media/aFfYlsEdiWPDi/giphy.gif")
        embed.set_footer(text=choice(common.facts))

        embed.add_field(name="CPU", value="[{0}]({1})".format(self.cpu,
                                                              "https://www.skroutz.gr/search?keyphrase=" + str(
                                                                  self.cpu).replace(' ', '%20')))
        if self.gpu:
            embed.add_field(name="GPU", value="[{0}]({1})".format(self.gpu,
                                                                  "https://www.skroutz.gr/search?keyphrase=" + str(
                                                                      self.gpu).replace(' ', '%20')))

        embed.add_field(name="Mo/Bo", value="[{0}]({1})".format(self.mobo,
                                                                "https://www.skroutz.gr/search?keyphrase=" + str(
                                                                    self.mobo).replace(' ', '%20')))
        embed.add_field(name="RAM", value="[{0}]({1})".format(self.ram,
                                                              "https://www.skroutz.gr/search?keyphrase=" + str(
                                                                  self.ram).replace(' ', '%20')))
        embed.add_field(name="PSU", value="[{0}]({1})".format(self.psu,
                                                              "https://www.skroutz.gr/search?keyphrase=" + str(
                                                                  self.psu).replace(' ', '%20')))
        if self.ssd:
            embed.add_field(name="SSD", value="[{0}]({1})".format(self.ssd,
                                                                  "https://www.skroutz.gr/search?keyphrase=" + (
                                                                      self.ssd).replace(' ', '%20')))
        if self.hdd:
            embed.add_field(name="HDD", value="[{0}]({1})".format(self.hdd,
                                                                  "https://www.skroutz.gr/search?keyphrase=" + str(
                                                                      self.hdd).replace(' ', '%20')))
        if self.case:
            embed.add_field(name="Case", value="[{0}]({1})".format(self.case,
                                                                   "https://www.skroutz.gr/search?keyphrase=" + str(
                                                                       self.case).replace(' ', '%20')))
        if self.cooler:
            embed.add_field(name="Cooler", value="[{0}]({1})".format(self.cooler,
                                                                     "https://www.skroutz.gr/search?keyphrase=" + str(
                                                                         self.cooler).replace(' ', '%20')))

        # if self.comment :
        #     out += '\n' + self.comment + '\n'
        return embed


class Monitor(models.Model):
    price = models.IntegerField(blank=False)
    name = models.CharField(max_length=64, blank=False, unique=True)
    url = models.URLField(blank=True, unique=True)
    resolution = models.CharField(
        max_length=16,
        blank=False,
        choices=(
            ('1080p', '1080p'),
            ('1440p', '1440p'),
            ('4K', '4K'),
            ('Ultrawide', 'Ultrawide'),
        ),
    )
    panel = models.CharField(max_length=16, blank=True)
    refresh_rate = models.IntegerField(default=60)

    def publish(self):
        self.save()

    def __str__(self):
        return self.name + ' ' + str(self.price) + '€ ' + self.get_resolution_display() + ' ' + str(
            self.refresh_rate) + 'Hz(1/s)'


class UserBuild(models.Model):
    discord_id_validator = RegexValidator(r'\d{18}', 'Only numeric characters are allowed.')

    name = models.CharField(max_length=64, blank=True)
    owner = models.CharField(blank=True, max_length=18, validators=[discord_id_validator])

    pc = models.OneToOneField(Pc, on_delete=models.CASCADE)
    monitor = models.OneToOneField(Monitor, blank=True, null=True, on_delete=models.CASCADE)

    message = models.TextField(blank=True)

    def publish(self):
        self.save()

    def __str__(self):
        return self.name + ' ' + self.owner

    def getSpecs(self):
        return self.pc.getSpecs()


class Helper(models.Model):
    name = models.CharField(max_length=128, unique=True)
    content = models.TextField()

    def publish(self):
        self.save()

    def __str__(self):
        return self.name

    def get_embed(self):
        e = common.generate_embed(self.name, self.content)
        return e


class Peripheral(models.Model):
    price = models.IntegerField(blank=False)
    name = models.CharField(max_length=64, unique=True)
    url = models.URLField(unique=True)

    type = models.IntegerField(
        blank=False,
        choices=(
            (1, 'Mouse'),
            (2, 'Keyboard'),
            (3, 'Headset'),
        ),
        default=1
    )

    def publish(self):
        self.save()

    def __str__(self):
        return self.name
