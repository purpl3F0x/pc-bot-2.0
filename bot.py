# bot.py

import discord
import asyncio
import os

import builds
#import monitors


##########################################################
##########################################################
# Dept. of Redundancy Department
# (2B || !2B) == true
# Which is a statement that's true and it's always correct
##########################################################
##########################################################

# Get Token from Heroku env. vars
# you now it helps not to print your private keys
token = os.environ['TOKEN']


whitelist = [
    "466149664383565827",   # test server
    "418758155078598666",   # gramers
    "468208302875213825",   # meh
]


def RepresentsInt(s):
    '''Check if a string is an interger'''
    try:
        int(s)
        return True
    except ValueError:
        return False


client = discord.Client()  # init connection to server


# Well my code has met greater days but... It gets the job done for now

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


####### Thiz is were magik bigens :P :P
@client.event
async def on_message(message):
    print(message.content)

    if message.content.startswith('!pc') and (message.channel.id in whitelist):
        if message.content == ('!pc all'):  # That's for debuging only
            for b in builds.builds:
                await client.send_message(message.channel, str(b))
            await client.send_message(message.channel,
                                      '<@!133245022719049728> someone is asking for trouble {0.author.mention}'.format(
                                          message))

        # Split message arguments
        args = message.content.split(" ")
        args = args[1:]
        msg = ''
        if len(args) and RepresentsInt(args[0]):  # Make sure first args is price
            if len(message.mentions):  # See if user is mentioned
                await client.send_message(message.channel, message.mentions[0].mention)

            answer = builds.builds[builds.getClosest(int(args[0]))].getSpecs()  # Get the best match
            msg += str(answer)  # Send the build
            await client.send_message(message.channel, msg)  # Wait to send messege to server

        else:  # Message is not properly formated
            await client.send_message(message.channel,
                                      'I am sorry {0.author.mention}, I am afraid I can\'t let you do that'.format(
                                          message))


    elif message.content.startswith('!oscar'):  # Rest is a good thing from time to time
        await asyncio.sleep(10)
        await client.send_message(message.channel,
"""Thank <@!133245022719049728> for giving me life (coding) :purple_heart: :purple_heart: :purple_heart: !,
Thank <@!372150009694650370>  my mother for doing nothing, nothing at all ,0 :cat: ,
Thank <@!419166458489339935> for giving me food :apple: (making the builds)
"""
                                  )


    # yeah it's not copy paste, not at all
    elif message.content.startswith('!monitor') or message.content.startswith('!mon '):
        if message.content == ('!monitor all'):  # That's for debuging only
            for b in monitors_list.monitors_list:
                await client.send_message(message.channel, str(b))

        # Split message arguments
        args = message.content.split(" ")
        args = args[1:]
        msg = ''
        if len(args) and RepresentsInt(args[0]):  # Make sure first args is price
            if len(message.mentions):  # See if user is mentioned
                await client.send_message(message.channel, message.mentions[0].mention)

            answer = monitors_list.monitors_list[monitors_list.getClosest(int(args[0]))]  # Get the best match
            msg += str(answer)  # Send the build
            await client.send_message(message.channel, msg)  # Wait to send messege to server
        else:
            await client.send_message(message.channel,
                                      'I am sorry {0.author.mention}, I am afraid I can\'t let you do that'.format(
                                          message))
    elif message.content.startswith('!update'):
        builds.update()
        await client.send_message(message.channel,
                                  'Yummy, Yummy, Yummy I got some new stuff :P'
                                 )

if __name__ == "__main__":
    # bot = false case it's FUCKING user, not bot!
    client.run(
        token,
        bot=False
    )

################################
####### That's all folks #######
################################
