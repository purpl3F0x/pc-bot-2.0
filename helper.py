# Stavros Avramidis
# helper.py

import os
import re

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


def is_mention(s):
    if re.match(r"<@!?\d{18}>", s):
        return s[2:20]
    return False
