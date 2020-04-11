#libraries to pip install
import discord #see discord.py for installation
import asyncio
from discord.ext import commands

import BotClass as bc
import Token as Token #this is a separate file contaning the token


client = commands.Bot(command_prefix = '+')
bot_obj = None


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

#Connects to a server
@client.command(pass_context=True)
async def connect(ctx):
    global bot_obj
    if ctx.message.author.voice != None:
        if bot_obj == None:
            name = ctx.message.author
            bot_obj = bc.Sbb(name)

        channel = ctx.message.author.voice.channel
        if not bot_obj.is_connected:
            connected_to = await channel.connect()
            bot_obj.is_connected = True
            bot_obj.channel = connected_to
            bot_obj.voice_channel = channel

        elif channel != bot_obj.voice_channel:
            await disconnect(ctx)
            connected_to = await channel.connect()
            bot_obj.channel = connected_to
            bot_obj.voice_channel = channel
            bot_obj.is_connected = True
    else:
        print("no server to join")


#Disconnects to a server
@client.command(pass_context=True)
async def disconnect(ctx):
    global bot_obj
    await ctx.voice_client.disconnect()
    bot_obj.is_connected = False
    bot_obj.channel = None



@client.command(pass_context=True)
async def play(ctx, file_name):
    global bot_obj
    filename = file_name + ".mp3"
    calling_user = ctx.message.author
    voice_channel = calling_user.voice.channel
    if voice_channel != None:
        await connect(ctx)
        if not bot_obj.is_playing:
            bot_obj.queue.append(filename)
            bot_obj.is_playing = True

            while (True):
                bot_obj.channel.play(discord.FFmpegPCMAudio('./audio_files/' + bot_obj.queue[0]))
                print(client.voice_clients[0].is_playing())

                while True:
                    await asyncio.sleep(1)
                    print(client.voice_clients[0].is_playing())
                    if not client.voice_clients[0].is_playing():
                        break

                print("done playing: ", bot_obj.queue[0])
                await asyncio.sleep(0.5)
                sek_counter = 0
                bot_obj.queue.pop(0)
                if len(bot_obj.queue) == 0:
                    break
            print("nothing more to play")
            bot_obj.is_playing = False

        else:
            bot_obj.queue.append(filename)

#used for the bot to download files sent to the bot
@client.command(pass_context = True)
async def download(ctx):
    message = ctx.message
    if not message.attachments == [] and ".mp3" in message.attachments[0].filename:
        attachment = message.attachments[0]
        print(attachment.filename, " ::: ", attachment.url)
        file_name = attachment.filename
        await attachment.save(path to here /audio_file)
    else:
        print("no file attached")

@client.command(pass_context=True)
async def exit(ctx):
    global bot_obj
    bot_obj = None
    await client.close()


token = Token.get_token()
client.run(token)
