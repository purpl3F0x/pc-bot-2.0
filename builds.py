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


def getClosest(d, args=[]):  # Find Build with the closest price
    if args:
        tags = lists.models.Tag.objects.all().filter(val__in=args)
        if tags:
            builds = lists.models.Pc.objects.all().filter(tags__in=tags)
        else:
            builds = lists.models.Pc.objects.all().filter(active=True)
    else:
        builds = lists.models.Pc.objects.all().filter(active=True)

    prices = [b.price for b in builds]
    m = min(prices, key=lambda x: abs(x - int(d)))
    return builds[prices.index(m)]


def getUserBuild(name="",user_id=""):
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




if __name__ == "__main__":
    print(42 * '_')

    a = getClosest(4217)
    print(a)

    a = getClosest(4217, ["AMD"])

    all = getAll()
    print (all)

    print(a)


    #### user Builds

    a = getUserBuild(name="test")
    print(a)
    a = getUserBuild(name="Test")
    print(a)

    a = getUserBuild(user_id="133245022719049728")
    print(a)
