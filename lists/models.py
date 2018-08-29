from django.db import models
from django.utils import timezone


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

    def getSpecs(self):                    # Oh this is going to be a messsh!
        out=''

        out += str(self.price) + '€\n'
        out += '-'*42 + '\n'
        out += 'CPU: ' + self.cpu + '\n'  

        if self.gpu :
            out += 'GPU: ' + self.gpu + '\n'  

        out += 'Mobo: ' + self.mobo + '\n'
        out += 'RAM: ' + self.ram + '\n'
        out += 'PSU: ' + self.psu + '\n'

        if self.ssd :
            out += 'SSD: ' + self.ssd + '\n'
        if self.hdd :
            out += 'HDD: ' + self.hdd + '\n'
        if self.case :
            out += 'Case: ' + self.case + ' (Recommended)\n'
        if self.cooler :
            out += 'Cooler: ' + self.cooler + '\n'
        if self.comment :
            out += '\n' + self.comment + '\n'

        return out




class Monitor(models.Model):
    price = models.IntegerField(blank=False)
    name = models.CharField(max_length=64,blank=False)
    resolution = models.CharField(max_length=16,blank=False,
                                  choices=(
                                      (1, '1080p'),
                                      (2, '1440p'),
                                      (3, '4K'),
                                  ), default=1)
    panel = models.CharField(max_length=16,blank=True)
    refresh_rate = models.IntegerField(default=60)


    
    def publish(self):
        self.save()

    def __str__(self):
        return self.name + ' ' + str(self.price) + '€ ' + self.resolution + ' ' + str(self.refresh_rate) + 'Hz(1/s)'
