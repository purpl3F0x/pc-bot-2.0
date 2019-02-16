# Stavros Avramidis
# bot.py
# v3.0 - The new Generation

import os
import re

import discord
from discord.ext.commands import Bot

# local imports
import builds
import disc_admin
import quotes

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

    print(context.message.channel.id, 'Requested: ')
    print('args: ', args)
    print('price :', price)

    answer = builds.getClosest(price, args)

    await bot.say(embed=answer.getemded())

    # if answer:
    #     await bot.say(answer.getspecs())
    # else:
    #     await bot.say(":thinking: :hugging: :fox: ")

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
async def pc_info(context):
    # Check if message in whitelisted channel
    if context.message.channel.id not in whitelist:
        return

    if context.message.author.id in disc_admin.getBlackList():
        await bot.say(
            "I'm sorry <@" + context.message.author.id + "> ,guess who is on black list"
        )
        return

    res = """Thank <@!133245022719049728> for giving me life :purple_heart: :purple_heart: :purple_heart:
        Thank <@!419166458489339935> for giving me food :apple:
        Thank <@!332970862150156289> for cleaning my :poop:

        https://github.com/purpl3F0x/pc-bot-2.0
        **Pc Bot v3.1 #I wanna be forever young!**
        Hey!! now I'm a :metal: :star2: ...also the roof is on fire,
        
        **You and me baby ain't nothin' but mammals...
        ...So let's do it like they do on the Discovery Channel**
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


@bot.command(pass_context=False)
async def hal(*args):
    for i in range(len(args)):
        if is_mention(args[i]):
            del args[i]

    retURL = 'http://lmgtfy.com/?q=%s' % "+".join(args)

    embed = discord.Embed(description=" [%s](%s)" % (" ".join(args), retURL), color=0x836cff)
    # embed.set_thumbnail(url="http://www.patriotsanon.com/images/hal9000.gif")
    embed.set_footer(text="'Cause I'm just a teenage dirtbag, baby...")
    await bot.say(embed=embed)


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
            name="Can't Let You do DAT"
        )
    )


###############################################
###############################################
###############################################


# Let the Magik begin

if __name__ == "__main__":
    # bot = false case it's FUCKING user, not bot!
    bot.run(
        token,
        bot=False
    )

###############################################
############## That's all folks  ##############
###############################################
