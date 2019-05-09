from django.db import models
from markdownx.models import MarkdownxField

import common as common
import parts.models


class Build(models.Model):
    name = models.CharField(blank=True, max_length=64)

    cpu = models.ForeignKey(parts.models.CPU, blank=False, on_delete=models.PROTECT)
    motherboard = models.ForeignKey(parts.models.Motherboard, blank=False, on_delete=models.PROTECT)
    ram = models.ForeignKey(parts.models.RAM, blank=False, on_delete=models.PROTECT)
    gpu = models.ForeignKey(parts.models.GPU, blank=True, null=True, on_delete=models.PROTECT)
    psu = models.ForeignKey(parts.models.PSU, blank=False, on_delete=models.PROTECT)
    cooler = models.ForeignKey(parts.models.Cooler, blank=True, null=True, on_delete=models.PROTECT)
    case = models.ManyToManyField(parts.models.Case, blank=True)
    others = models.ManyToManyField(parts.models.Part, blank=True)
    price = models.IntegerField(blank=True, default=0)
    description = MarkdownxField(blank=True)

    def update_price(self, force=False):
        """
        Updates object price

        :param force: forces update all objects (depreciated)y
        :return:
        """
        # Price is all items that are required in model
        self.price = self.cpu.price + self.motherboard.price + self.ram.price + self.psu.price
        # price of gpu if any
        self.price += self.gpu.price if self.gpu else 0
        # price of cooler if any
        self.price += self.cooler.price if self.cooler else 0
        # average price of cases
        if self.case.all().count():
            self.price += (sum([case.price for case in self.case.all()]) / self.case.all().count())
        # Price of accessories
        self.price += sum([c.price for c in self.others.all()])

    def save(self, *args, **kwargs):
        super(Build, self).save(*args, **kwargs)
        self.update_price()
        super(Build, self).save(*args, **kwargs)

    def publish(self):
        self.save()

    def __str__(self):
        return self.name if self.name else str(self.cpu) + ' ' + str(self.price)

    def get_as_embed(self) -> common.Embed:
        """
        Generates a Discord embed object

        :return: discord.Embed
        """
        embed = common.generate_embed(
            title=self.name,
            description=self.description if self.description else 'rand_quote',
            add_images=True
        )

        embed.set_author(name=str(self.price) + ' 💶', url=common.hal_url, icon_url=common.hal_gif)

        def markdown_url(text, url):
            return '[%s](%s)' % (str(text), str(url))

        embed.add_field(name="CPU", value=markdown_url(self.cpu.clean_name(), self.cpu.url), inline=True)

        embed.add_field(name="RAM", value=markdown_url(self.ram.clean_name(), self.ram.url), inline=True)

        embed.add_field(name="Motherboard", value=markdown_url(self.motherboard.clean_name(), self.motherboard.url),
                        inline=True)
        embed.add_field(name="GPU", value=markdown_url(self.gpu.clean_name(), self.gpu.url) if self.gpu else 'igpu',
                        inline=True)
        embed.add_field(name="PSU", value=markdown_url(self.psu.clean_name(), self.psu.url), inline=True)

        embed.add_field(name="Cooler",
                        value=markdown_url(self.cooler.clean_name(), self.cooler.url) if self.cooler else 'stock',
                        inline=True)

        for o in self.others.all():
            embed.add_field(name=o.description, value=markdown_url(o.clean_name(), o.url), inline=True)

        if self.case.count():
            embed.add_field(name="📦", value='Some cases to see', inline=False)
            for c in self.case.all():
                embed.add_field(name='🙊', value=markdown_url(c.clean_name(), c.url), inline=False)

        return embed


class Monitor(models.Model):
    price = models.IntegerField(blank=False)
    name = models.CharField(max_length=64, blank=False, unique=True)
    url = models.URLField(blank=True)
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
