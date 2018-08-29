# bot.py
# v 2.0 -beta

import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import os

# local imports
import builds


##########################################################
##########################################################
# Dept. of Redundancy Department
# (2B || !2B) == true
# Which is a statement that's true and it's always correct
##########################################################
##########################################################


# Server channels whitelist
whitelist = [
    "466149664383565827",   # test server main
    "418758155078598666",   # gramers-sklhra
    "468208302875213825",   # meh
    "467344493449052170",   # test server  beta
]

# initialise bot
bot = Bot(command_prefix='$')

token = os.environ['TOKEN']



###############################################
###############################################
###############################################

@bot.command(pass_context=True)
async def pc(context, price: int, *args):
    ''''''
    # Check if message in whitelisted channel
    if context.message.channel.id not in whitelist:
        return
    print(context.message.channel.id, 'Requested: ')
    print('args: ', args)
    print('price :', price)

    answer =  builds.\
        getClosest(price,args).\
        getSpecs()

    if answer:
        await bot.say(answer)
    else:
        await bot.say(":thinking: :hugging: :fox: ")

    return

###############################################

@bot.command(pass_context=True)
async def pc_info(context):
    # Check if message in whitelisted channel
    if context.message.channel.id not in whitelist:
        return

    await bot.say(
        """Thank <@!133245022719049728> for giving me life (coding) :purple_heart: :purple_heart: :purple_heart: !,
        Thank <@!419166458489339935> for giving me food :apple: (making the builds)
        Thank <@!332970862150156289> for cleaning my :poop:
        Thank <@!372150009694650370>  my mother for doing nothing, nothing at all ,0 :cat: ,
        
        https://github.com/purpl3F0x/pc-bot-2
        `Pc Bot v2.0-beta`
        """
    )

    return

###############################################

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-'*42)


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

"""
Home
A place where I can go
To take this off my shoulders
Someone take me home
Someone take me
"""

###############################################
############## That's all folks  ##############
###############################################