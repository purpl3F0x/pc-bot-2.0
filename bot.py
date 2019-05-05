# Stavros Avramidis
# bot.py
# v3.2 - The new Generation

import logging
import os
import re
import time

import discord
from discord.ext.commands import Bot

# local imports
import builds
import disc_admin
import helper
import quotes
import skroutz_scrapper as skrtz
from lists.common import generate_embed

##########################################################
##########################################################
# Dept. of Redundancy Department
# (2B || !2B) == true
# Which is a statement that's true and it's always correct
##########################################################
##########################################################


# Server channels whitelist
whitelist = [
    "466149664383565827",  # test server main
    "418758155078598666",  # gramers-sklhra
    "468208302875213825",  # meh
    "467344493449052170",  # test server  beta
]

# initialise bot
bot = Bot(command_prefix='$')

# get bot token from env vars
token = os.environ['TOKEN']


############ Some helper funcitons ############
def is_mention(s):
    if re.match("<@+\d{18}>", s):
        return s[2:20]

    return False


###############################################
###############################################
###############################################

@bot.command(pass_context=True)
async def pc(context, price: int, *args):
    # Check if message in whitelisted channel
    if context.message.channel.id not in whitelist:
        return

    if context.message.author.id in disc_admin.getBlackList():
        await bot.add_reaction(context.message, '\U0001F622')
        await bot.add_reaction(context.message, '\U0001F5A4')
        await bot.add_reaction(context.message, '\U0001F4DD')
        return

    answer = builds.getClosest(price, args)

    await bot.say(embed=answer.getemded())

    return


###############################################

@bot.command(pass_context=True)
async def build(context, arg, *args):
    # Check if message in whitelisted channel
    if context.message.channel.id not in whitelist:
        return

    if context.message.author.id in disc_admin.getBlackList():
        await bot.add_reaction(context.message, '\U0001F622')
        await bot.add_reaction(context.message, '\U0001F5A4')
        await bot.add_reaction(context.message, '\U0001F4DD')
        return

    if is_mention(arg):
        print(is_mention(arg))
        answer = builds.getUserBuild(
            user_id=is_mention(arg)
        )

    else:
        answer = builds.getUserBuild(
            name=arg
        )

    print(answer)

    if answer:
        await  bot.say(answer.getSpecs())
        if answer.monitor:
            await bot.say(answer.monitor)
        if answer.message:
            await bot.say(answer.message)

    return


###############################################


@bot.command(pass_context=True)
async def pc_all(context, min: int = 0, max: int = 1000000000, *args):
    # Check if message in whitelisted channel
    if context.message.channel.id not in whitelist:
        return

    if context.message.author.id not in disc_admin.getAdminsId():
        await bot.say(
            "I'm sorry <@" + context.message.author.id + "> ,I'm afraid I can't let you do that!\nI only obey my Daddy:purple_heart::fox: and his minions"
        )
        return

    answer = builds. \
        getAll(min, max)

    if answer:
        for b in answer:
            await bot.say(
                b.getSpecs()
            )
    else:
        await bot.say(":thinking: :hugging: :fox: ")

    return


###############################################


@bot.command(pass_context=True)
async def info(context):
    # Check if message in whitelisted channel
    if context.message.channel.id not in whitelist:
        return

    if context.message.author.id in disc_admin.getBlackList():
        await bot.add_reaction(context.message, '\U0001F622')
        await bot.add_reaction(context.message, '\U0001F5A4')
        await bot.add_reaction(context.message, '\U0001F4DD')
        return

    res = """Thank ***Purpl3F0x*** for giving me life :purple_heart: :purple_heart: :purple_heart:
        Thank ***wiz*** for giving me food :apple:
        Thank ***Mand Break*** for cleaning my :poop:
        
        __Version 3.2__

        https://github.com/purpl3F0x/pc-bot-2.0
        *I want you
        To be
        Left behind those empty walls
        Don't
        You see
        From behind those empty walls
        Those empty walls
        When we decline, from the confines of our mind
        Don't waste your time, on coffins today*
        """

    embed = discord.Embed(description=res, color=0x836cff)
    await bot.say(embed=embed)

    return


###############################################

@bot.command(pass_context=True)
async def blacklist(context, member: discord.Member, reason=""):
    # Check if message in whitelisted channel
    if context.message.channel.id not in whitelist:
        return

    if context.message.author.id not in disc_admin.getAdminsId():
        await bot.say(
            "I'm sorry <@" + context.message.author.id + "> ,I'm afraid I can't let you do that!\nI only obey my Daddy:purple_heart::fox: and his minions"
        )
        return

    disc_admin.blackListuser(member.id, reason)

    await bot.add_reaction(context.message, '\U0001F44D')

    return


###############################################


@bot.command(pass_context=True)
async def hal(context, *args):
    if context.message.channel.id not in whitelist:
        return

    for i in range(len(args)):
        if is_mention(args[i]):
            del args[i]

    retURL = 'http://lmgtfy.com/?q=%s' % "+".join(args)

    embed = discord.Embed(description=" [%s](%s)" % (" ".join(args), retURL), color=0x836cff)
    # embed.set_thumbnail(url="http://www.patriotsanon.com/images/hal9000.gif")
    embed.set_footer(text="'Cause I'm just a teenage dirtbag, baby...")
    await bot.say(embed=embed)


###############################################


@bot.command(pass_context=True)
async def helpme(context, *, arg):
    h = helper.helperFuzzy(arg)
    if h is not None:
        await bot.say(embed=h.get_embed())
    return


###############################################

skroutz_cmd_arg = {'--desc', '--asc'}
lxr = {'desc': {'order_dir': 'desc'}, 'asc': {'order_dir': 'asc'}, 'price': {'order_by': 'pricevat'},
       'pop' : {'order_by': 'popularity'}}


@bot.command(pass_context=True)
async def skroutz(context, *args):
    start = time.time()
    cmd_args, q_args = [], []
    for x in args:
        (q_args, cmd_args)[x.startswith('--')].append(x)
        if x.startswith('--help'):
            await bot.say(
                "```php\nskroutz HALP\n\n<optional args>\n'--pop':         sort by popularity (default)\n'--price':       sort by price\n'--asc':         sort by ascending order( raises --price by default)\n'--desc':        sort by descending order( raises --price by default)\n'--max-{int}':   maximum price\n'--min-{int}':   minimun price\n'--help':        shows this dah :|\n\nex: '$skroutz 2080 --asc --min-750'\n```")
            return

    d = {}
    for arg in cmd_args:
        arg = arg[2:].lower()
        if arg in lxr:
            d.update(lxr[arg])
        elif arg.startswith('max'):
            try:
                d.update({'price_max': int(arg[4:])})
            except ValueError:
                continue
        elif arg.startswith('min'):
            try:
                d.update({'price_min': int(arg[4:])})
            except ValueError:
                continue

    if not q_args:
        await bot.add_reaction(context.message, '\U0001F622')
        return
    query = "+".join(q_args)
    url = skrtz.search_url + query
    res, msg = skrtz.get_product_page(url, args=d)
    if not res:
        await bot.add_reaction(context.message, '\U0001F623')
    else:
        ans = generate_embed("Query Results Thank ~~GOD~~ HAL", add_images=False)
        ans.description += '\n\n'
        ans.description += "[{0}]({1})\n\n:star:\n\_ \_ \_ \_ \_ \_ \_ \_ \_ \_ \_ \_ \_ \_".format(msg, url)
        for r in res:
            ans.add_field(name=r['name'], value="[{0}]({1})".format(str(r['price']) + ' :euro:', r['url']),
                          inline=False)

        ans.add_field(name="|query took|", value='{}'.format(time.time() - start), inline=False)

        await bot.say(embed=ans)
    return


###############################################

@bot.command(pass_context=True)
async def per(context, tp, price: int, *args):
    tp = tp.lower()
    res = []

    if tp == 'mouse':
        res = builds.get_peripheral(price, '1')
    elif tp == 'keyboard':
        res = builds.get_peripheral(price, '2')
    elif tp == 'headset':
        res = builds.get_peripheral(price, '3')

    if not res:
        await bot.add_reaction(context.message, '\U0001F623')
        return

    e = generate_embed(add_images=False)

    for _ in res:
        e.add_field(name=_.name, value="[{0}]({1})".format(str(_.price) + ' :euro:', _.url), inline=False)

    await bot.say(embed=e)

    return


###############################################


@bot.command(pass_context=True)
async def monitor(context, price: int, resoluton: str = '', refresh_rate: int = 0, *args):
    res = builds.get_monitor(price, resoluton, refresh_rate)

    if not res:
        await bot.add_reaction(context.message, '\U0001F623')
        return

    e = generate_embed(
        title='{}€ {} {} monitors'.format(
            price,
            resoluton,
            (str(refresh_rate) + ' Hz' if refresh_rate else str())
        ),
        add_images=False
    )

    for _ in res:
        e.add_field(
            name=_.name,
            value="[{0}]({1})".format(
                str(_.price) + ' :euro:',
                _.url if _.url else ('https://www.skroutz.gr/search?keyphrase=' + _.name.replace(' ', '+'))
            ),
            inline=False
        )

    await bot.say(embed=e)

    return


###############################################


@bot.event
async def on_message(message):
    if message.channel.is_private and message.author.id != bot.user.id and message.channel.id != "468208302875213825":
        quote = quotes.quote().replace(
            "%user",
            ("<@" + message.author.id + ">")
        )
        await bot.send_message(message.channel, quote)
    else:
        # Check if message in whitelisted channel
        if message.channel.id not in whitelist:
            return
        logging.info((str(__import__('time').time()) + " " + message.author.id + " : " + str(message.content)))
        await bot.process_commands(message)

    return


###############################################


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-' * 42)

    # Set rich presence
    await bot.change_presence(
        game=discord.Game(
            name="I'm Sorry Dave!"
        )
    )


###############################################
###############################################
###############################################


# Let the Magik begin

if __name__ == "__main__":
    # bot = false case it's FUCKING user, not bot!
    handler = logging.FileHandler("hal.log", "a", encoding="UTF-8")
    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)

    bot.run(
        token,
        bot=False
    )

###############################################
############## That's all folks  ##############
###############################################
