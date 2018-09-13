from django.core.validators import RegexValidator
from django.db import models


# Create your models here.

class Admin(models.Model):
    discord_id_validator = RegexValidator(r'\d{18}', 'Only numeric characters are allowed.')

    discord_id = models.CharField(unique=True, max_length=18, validators=[discord_id_validator])

    name = models.CharField(max_length=32, blank=True)

    def publish(self):
        self.save()

    def __str__(self):
        return self.discord_id + (" (" + self.name + ")" if self.name else "")

    def mention(self):
        return "<@" + self.discord_id + ">"


class BlackUser(models.Model):
    discord_id_validator = RegexValidator(r'\d{18}', 'Only numeric characters are allowed.')

    discord_id = models.CharField(unique=True, max_length=18, validators=[discord_id_validator])

    reason = models.TextField(max_length=128, blank=True)

    def publish(self):
        self.save()

    def __str__(self):
        return self.discord_id
