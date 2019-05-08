# Stavros Avramidis
# helper.py

import os

import django
from fuzzywuzzy import fuzz

import lists

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pc_bot.settings")
django.setup()


def helperFuzzy(inStr):
    helpers = lists.models.Helper.objects.all()
    for h in helpers:
        if fuzz.partial_ratio(h.name, inStr) > 80:
            return h
    return None
