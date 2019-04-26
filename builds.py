# Stavros Avramidis
# builds.py

import os

import django

import lists

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pc_bot.settings")
django.setup()


def update():
    print('Updating builds query')
    global builds
    builds = lists.models.Pc.objects.all()
    return len(builds)


def getAll(min=0, max=100000000):

    return lists.models.Pc.objects.all().filter(price__gte=min, price__lte=max)


def getClosest(price: int, args: list = []):
    """
    Returns the closest in price build
    :param price:   target price
    :param args:    optional args as filters
    :return:        returns a Pc object from models
    """
    if args:
        tags = lists.models.Tag.objects.all().filter(val__in=args)
        if tags:
            builds = lists.models.Pc.objects.all().filter(tags__in=tags)
        else:
            builds = lists.models.Pc.objects.all().filter(active=True)
    else:
        builds = lists.models.Pc.objects.all().filter(active=True)

    prices = [b.price for b in builds]
    m = min(prices, key=lambda x: abs(x - int(price)))
    return builds[prices.index(m)]


def getUserBuild(name="", user_id=""):
    if name:
        try:
            return lists.models.UserBuild.objects.get(name=name)
        except:
            return None

    elif user_id:
        try:
            return lists.models.UserBuild.objects.get(owner=user_id)
        except:
            return None

    return None


def get_peripheral(price: int, type):
    m = lists.models.Peripheral.objects.all().filter(type__in=type)
    out = list(filter(lambda x: abs(x.price - price) < 7, m))
    return out


######################################
######################################
######################################
######################################


if __name__ == "__main__":
    print(get_peripheral(43, '1'))

    exit(0)
    print(42 * '_')

    a = getClosest(4217)
    print(a)

    a = getClosest(4217, ["AMD"])

    all = getAll()
    print(all)

    print(a)

    #### user Builds

    a = getUserBuild(name="test")
    print(a)
    a = getUserBuild(name="Test")
    print(a)

    a = getUserBuild(user_id="133245022719049728")
    print(a)
