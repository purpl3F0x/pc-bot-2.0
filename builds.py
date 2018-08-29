# Stavros Avramidis
# builds.py

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pc_bot.settings")

import django

django.setup()

import lists


def update():
    print('Updating builds query')
    global builds
    builds = lists.models.Pc.objects.all()
    return len(builds)


def getClosest(d, args=[]):  # Find Build with the closest price
    if args:
        tags = lists.models.Tag.objects.all().filter(val__in=args)
        if tags:
            builds = lists.models.Pc.objects.all().filter(active=True, tags__in=tags)
        else:
            builds = lists.models.Pc.objects.all().filter(active=True)
    else:
        builds = lists.models.Pc.objects.all().filter(active=True)

    prices = [b.price for b in builds]
    m = min(prices, key=lambda x: abs(x - int(d)))
    return builds[prices.index(m)]


if __name__ == "__main__":
    print(42 * '_')

    a = getClosest(4217)
    print(a)

    a = getClosest(4217, ["AMD"])

    print(a)
