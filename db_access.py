# Stavros Avramidis
# db_access.py

import os

import django
from fuzzywuzzy import fuzz

import discord_admin
import lists

# setup connection with django db
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pc_bot.settings")
django.setup()


def get_builds(price: int) -> list:
    """
    Finds builds close to target price (within 10%)
    :param price: target price
    :return: list of lists.models.Build objects
    """
    return list(filter(
        lambda x: abs(x.price - price) < price * .1 + 5,
        lists.models.Build.objects.all()
    ))


def get_peripheral(price: int, type):
    """
    Finds peripherals close to given price (within 12%)
    :param price: target price
    :param type: type of peripheral
    :return: list of lists.models.Peripheral objects
    """
    m = lists.models.Peripheral.objects.all().filter(type__in=type)
    out = list(filter(lambda x: abs(x.price - price) < price * .12, m))
    return out


def get_monitor(price: int, resolution: str = '', refresh_rate: int = 0):
    """
    Finds monitors close to given price (within 25% max 42euros)
    :param price: target price
    :param resolution: resolution (optional)
    :param refresh_rate: refresh rate (optional)
    :return:
    """
    monitors = lists.models.Monitor.objects.all()
    if resolution != '':
        monitors = list(filter(lambda x: (x.resolution.lower() == resolution.lower()), monitors))
    if refresh_rate != 0:
        monitors = list(filter(lambda x: (x.refresh_rate >= refresh_rate), monitors))

    out = list(filter(lambda x: abs(x.price - price) < min(x.price >> 2, 42), monitors))
    return out


def helper_fuzzy_match(s):
    """
    Matches string to list.models.Helper object (80% accuracy)
    :param s:
    :return: list.models.Helper object or None
    """
    helpers = lists.models.Helper.objects.all()
    for h in helpers:
        if fuzz.partial_ratio(h.name, s) > 80:
            return h
    return None


def get_admins():
    """
    :return: admins ID list
    """
    return [i.discord_id for i in discord_admin.models.Admin.objects.all()]


def get_black_list():
    """
    returns id of all blacklisted users
    :return:
    """
    return [i.discord_id for i in discord_admin.models.BlackUser.objects.all()]


def black_list_user(user_id, reason=""):
    """
    Adds a user to Blacklist
    :param user_id: Discord ID
    :param reason:
    :return:
    """
    b = discord_admin.models.BlackUser(discord_id=user_id, reason=reason)
    try:
        b.save()
    except ...:
        pass


def get_allowed_channels():
    """
    Gets allowed channel form Django DB
    :return: list of strings containing channels discord id
    """
    return [c.discord_id for c in discord_admin.models.AllowedChannel.objects.all()]


if __name__ == "__main__":
    print(get_monitor(42, '4K'))
    a = get_monitor(42, '1080p')
    for i in a:
        print(i.resolution)

    exit(0)
    print(get_peripheral(43, '1'))

    exit(0)
    print(42 * '_')

    a = get_builds(4217)
    print(a)

    a = get_builds(4217)
