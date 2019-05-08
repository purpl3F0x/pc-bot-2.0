# Stavros Avramidis
# disc_admin.py

import os

import django

import discord_admin

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pc_bot.settings")
django.setup()


def get_admins():
    """
    :return: returns all admins ID
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
