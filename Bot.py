#libraries to pip install
import discord #see discord.py for installation
import asyncio
from discord.ext import commands

import BotClass as bc
import Token as Token #this is a separate file contaning the token


client = commands.Bot(command_prefix = '+')
queue = []

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

#Connects to a server
@client.command(pass_context=True)
async def connect(ctx):
    connected = False
    if ctx.message.author.voice != None:
        voice = ctx.message.author.voice
        channel = voice.channel
        for i in client.voice_clients:
            if i.is_connected:
                connected = True
                if not i.channel == channel:
                    await i.move_to(channel)
                    break
        if not connected:
            await channel.connect()
    else:
        print("no server to join")


#Disconnects to a server
@client.command(pass_context=True)
async def disconnect(ctx):
    await ctx.voice_client.disconnect()



@client.command(pass_context=True)
async def play(ctx, file_name):
    global queue
    filename = file_name + ".mp3"
    calling_user = ctx.message.author
    voice_channel = calling_user.voice.channel
    if voice_channel != None:
        await connect(ctx)
        if not client.voice_clients[0].is_playing():
            queue.append(filename)
            while (True):
                client.voice_clients[0].play(discord.FFmpegPCMAudio('./audio_files/' + queue[0]))
                while True:
                    await asyncio.sleep(1)
                    if not client.voice_clients[0].is_playing():
                        break
                print("done playing: ", queue[0])
                await asyncio.sleep(0.5)
                sek_counter = 0
                queue.pop(0)
                if len(queue) == 0:
                    break
            print("nothing more to play")

        else:
            queue.append(filename)

#used for the bot to download files sent to the bot
@client.command(pass_context = True)
async def download(ctx):
    message = ctx.message
    if not message.attachments == [] and ".mp3" in message.attachments[0].filename:
        attachment = message.attachments[0]
        print(attachment.filename, " ::: ", attachment.url)
        file_name = attachment.filename
        await attachment.save("path to /audio_files/  here" + file_name)
    else:
        print("no file attached")

@client.command(pass_context=True)
async def exit(ctx):
    await client.close()


token = Token.get_token()
client.run(token)
