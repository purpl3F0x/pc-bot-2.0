import re
from random import choice

from discord import Colour, Embed

hal_url = 'http://3.120.5.250:8000/'
dave_gif = 'https://media.giphy.com/media/aFfYlsEdiWPDi/giphy.gif'
hal_gif = 'https://s3.amazonaws.com/gs-geo-images/356c3dd8-5d59-48cd-9a0b-5d638e6d48cd.gif'

captions = [
    "Stacy's mom has got it goin' on,\nhe's all I want and I've waited for so long",
    "And I know that you think it's just a fantasy\nBut since your dad walked out, your mom could use a guy like me",
    "I've got, nothing, to gain, to lose,\nAll the world I've seen before me passing by",
    "Hey you, see me, pictures crazy,\nAll the world I've seen before me passing by,",
    "Hey you, are me, not so pretty,\nAll the world I've seen before me passing by,"
    "You feel it runnin' through your bones\nAnd you jerk it out",
    "Her name is Noel,I have a dream about her\nShe rings my bell,I got gym class in half an hour",
    "Yeah I'm just a teenage dirt bag, baby. Listen to Iron Maiden, baby, with me, ooh",
    "And she doesn't give a damn about me\n'Cause I'm just a teenage dirt bag, baby",
    "Everybody's going to the party, have a real good time\nDancing in the desert, blowing up the sunshine",
    "Fear of the dark, fear of the dark, I have constant fear that something's always near",
    "Don't you see their bodies burning, Desolate and full of yearning, Dying of anticipation, Choking from intoxication",
    "Take my hand and let's end it all, She broke her little bones, on the boulders below !!",
    "Anti-depressants, Controlling tools of your system, Making life more tolerable",
]

facts = [
    'The marathon WR set by Eliud Kipchoge(16/9/2018) is 2:01:38 = 17\"/100m pace (can you do that dave?)',
    'In Sydney 10,000m final Haile Gebreselasie won by a 0.09 sec.(closer that the 100m final) with achilles tendon rupture',
    'Current 10000m WR set by Kenenisa Bekele is 26:17.5 and is 63\"/400m (57.09 last lap)',
    'Current 5000M WR set by Kenenisa Bekele is 12:17.5 and is 60\"/400m',
    'Eluid Kipchoge holds the seconds 2 fastest marathons ever ran',
    'Jim Walmsley set a new 50-Mile WR by running 80.4km at 3:36 m/km pace',
    'Highest ever recorded VO₂max is 96 mL/kg/min from Bjørn Dæhlie a xc-skier.'
]


def generate_embed(title: str = "", description: str = 'rand_quote', add_images: bool = True):
    if description is 'rand_quote':
        description = choice(captions)

    embed = Embed(title=title, colour=Colour(0x8567ff), url=hal_url,
                  description=description)
    if add_images:
        embed.set_thumbnail(url=dave_gif)
    embed.set_author(name="Hal", url="http://3.120.5.250:8000/",
                     icon_url=hal_gif)
    embed.set_footer(text=choice(facts))
    return embed


def is_mention(s):
    """
    Checks if a string is a user mention
    :param s:
    :return: returns the userID in case of mention else 0
    """
    if re.match(r"<@!?\d{18}>", s):
        return s[2:20]
    return 0


def split_mentions(l: list or tuple) -> (list, list):
    """
    Removes mentions from list of strings and returns both as separate lists
    :param l: list of strings
    :return: (arguments, mentions)
    """
    arguments, mentions = [], []
    for _ in l:
        (mentions if is_mention(_) else arguments).append(_)

    return arguments, mentions
