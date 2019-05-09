# # # # # # # # # # # # # # # # # # #
#                                   #
# @filename:    bot.py              #
# @author:      Stavros Avramidis   #
#                                   #
# # # # # # # # # # # # # # # # # # #

import logging
import os
import time

import discord
from discord.ext.commands import Bot

import common
# local imports
import db_access
import quotes
import skroutz_scrapper as skrtz
from common import generate_embed

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


###############################################
###############################################
###############################################

@bot.command(pass_context=True)
async def pc(context, price: int, *args):
    """
    Messages a build close to the given price
    :param context: msg context
    :param price: build target price
    :param args: optional arguments
    :return:
    """
    text, mentions = common.split_mentions(args)
    answer = db_access.get_builds(price)

    for i in answer:
        await bot.say(embed=i.get_as_embed())


@bot.command(pass_context=False)
async def info():
    """
    Prints bot info
    :return:
    """

    res = """Thank ***Purpl3F0x*** for giving me life :purple_heart: :purple_heart: :purple_heart:
        Thank ***wiz*** for giving me food :apple:
        Thank ***Mand Break*** for cleaning my :poop:
        
        **__Version 4.0-beta__**
        https://github.com/purpl3F0x/pc-bot-2.0
        
        *Peel me from the skin, tear me from the rind
        Does it make you happy now?
        Tear meat from the bone, tear me from myself
        Are you feeling happy now?*
        
        *Does it make you happy?
        Are you feeling happy?
        Are you fucking happy
        Now that I'm lost, left with nothing?*
        """

    embed = discord.Embed(description=res, color=0x836cff)
    await bot.say(embed=embed)

    return


@bot.command(pass_context=True)
async def blacklist(context, member: discord.Member, reason=""):
    """
    Adds a user to the blacklist
    :param context: msg context
    :param member: member mention
    :param reason: reason for banning (optional)
    :return:
    """

    if context.message.author.id not in db_access.get_admins():
        await bot.add_reaction(context.message, '\U0001F622')
        await bot.add_reaction(context.message, '\U0001F5A4')
        await bot.add_reaction(context.message, '\U0001F4DD')
        return

    db_access.black_list_user(member.id, reason)
    await bot.add_reaction(context.message, '\U0001F44D')


@bot.command(pass_context=True)
async def hal(context, *args):
    """
    The master command of trolls
    :param context: msg context
    :param args: list of command args
    :return:
    """
    text, mentions = common.split_mentions(args)

    url = "http://lmgtfy.com/?q=" + "+".join(text)

    embed = discord.Embed(description=" [%s](%s)" % (" ".join(text), url), color=0x836cff)
    embed.set_footer(text="\'Cause I'm just a teenage dirtbag, baby...")
    await bot.say(embed=embed)


@bot.command(pass_context=True)
async def helpme(context, *, arg):
    """
    Messages a helper, uses fuzzy match
    :param context: msg context
    :param arg: helper descriptions
    :return:
    """

    h = db_access.helper_fuzzy_match(arg)
    if h is not None:
        await bot.say(embed=h.get_embed())


@bot.command(pass_context=True)
async def skroutz(context, *args):
    """
    Searches skroutz for a product
    :param context: msg context
    :param args: product to search and optional arguments
    :return:
    """
    skroutz_cmd_arg = {'--desc', '--asc'}
    lxr = {'desc': {'order_dir': 'desc'}, 'asc': {'order_dir': 'asc'}, 'price': {'order_by': 'pricevat'},
           'pop' : {'order_by': 'popularity'}}
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
    """
    Messages a peripheral
    :param context:
    :param tp: type of peripheral
    :param price: target price
    :param args: optional args
    :return:
    """

    tp = tp.lower()
    res = []

    if tp == 'mouse':
        res = db_access.get_peripheral(price, '1')
    elif tp == 'keyboard':
        res = db_access.get_peripheral(price, '2')
    elif tp == 'headset':
        res = db_access.get_peripheral(price, '3')

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
async def monitor(context, price: int, resolution: str = '', refresh_rate: int = 0, *args):
    """

    :param context:
    :param price:
    :param resolution:
    :param refresh_rate:
    :param args:
    :return:
    """

    res = db_access.get_monitor(price, resolution, refresh_rate)

    if not res:
        await bot.add_reaction(context.message, '\U0001F623')
        return

    e = generate_embed(
        title='{}€ {} {} monitors'.format(
            price,
            resolution,
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


@bot.event
async def on_message(message):
    """
    Filters message before triggering commands
    :param message:
    :return:
    """
    if message.channel.is_private and message.author.id != bot.user.id and message.channel.id != "468208302875213825":
        quote = quotes.quote().replace("%user", ("<@" + message.author.id + ">"))
        await __import__('asyncio').sleep(2)
        await bot.send_message(message.channel, quote)
    else:
        # Check if message in whitelisted channel
        if message.channel.id not in whitelist:
            return
        logging.info((str(__import__('time').time()) + " " + message.author.id + " : " + str(message.content)))

        if message.author.id in db_access.get_black_list():
            await bot.add_reaction(message, '\U0001F622')
            await bot.add_reaction(message, '\U0001F5A4')
            await bot.add_reaction(message, '\U0001F4DD')
            return
        await bot.process_commands(message)

    return


###############################################


@bot.event
async def on_ready():
    """
    Listener function doing things when bot is connected
    :return:
    """
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
