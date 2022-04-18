

import discord
from os import getenv
from os import listdir
from os.path import isfile, join
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
from discord import FFmpegPCMAudio
import random


# Load the environment variables form the file
load_dotenv('./.env')

# Initialize Bot and Denote The Command Prefix
bot = commands.Bot(command_prefix="!")


# As soon as the bot is ready to use
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


# The command !index
@bot.command()
async def index(ctx):
    
    #  If the user who sent the command is in a voice channel
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()

        # Get all the voice lines in the file and generate a random number to get a different voiceline
        voiceLines = await getVoiceLines()
        index =  random.randint(0, len(voiceLines) - 1)

        # Set the source to the random voice line and play it
        source = FFmpegPCMAudio('./voicelines/' + voiceLines[index])
        voice.play(source)

        # While the player is not done playing put thread to sleep
        while voice.is_playing():
            await asyncio.sleep(1)

        # disconnect after the player has finished
        await voice.disconnect()
    else:
        await ctx.send("Unable to join voice channel as you are not in a voice channel")


# Gets all the file names in the voicelines directory
async def getVoiceLines():
    onlyfiles = [f for f in listdir('./voicelines') if isfile(join("./voicelines", f))]
    return onlyfiles



bot.run(getenv('TOKEN'))
