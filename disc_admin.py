# Stavros Avramidis
# disc_admin.py

import os

import django

import discord_admin

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pc_bot.settings")
django.setup()


def getAdminsId():
    return [i.discord_id for i in discord_admin.models.Admin.objects.all()]


def getBlackList():
    return [i.discord_id for i in discord_admin.models.BlackUser.objects.all()]


def blackListuser(user_id, reason=""):
    b = discord_admin.models.BlackUser(discord_id=user_id, reason=reason)
    try:
        b.save()
    except:
        pass

    return


if __name__ == "__main__":
    print(getAdminsId())
    print(getBlackList())

    blackListuser("133245022719049728", "dd")
