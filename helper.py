# Stavros Avramidis
# helper.py

import os

import django
from fuzzywuzzy import fuzz

from lists.models import Helper

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pc_bot.settings")
django.setup()


def helperFuzzy(inStr):
    helpers = Helper.objects.all()
    for h in helpers:
        if fuzz.partial_ratio(h.name, inStr) > 80:
            return {
                'name': h.name,
                'help': h.content
            }
    return None
