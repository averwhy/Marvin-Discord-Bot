import discord
import aiohttp
import time
from discord.ext import commands

TOKEN = 'token here'
userid = 'id here'
version = 'v1.1'
client = discord.Client()
ts = time.gmtime()

#The code in between these \/ hashtag lines are the classification detection code
###########################################################################################################################
#BIG THANKS TO ALBERTO POLIJAK FOR THE FOLLOWING CODE
    # Number separator is character between SCP and a number, example with hyphen:
    # SCP-1
NUMBER_SEPARATOR = "-"
MAXIMUM_SCP_NUMBER = 4999
def get_scp_link(message_content):
    word_list = message_content.split(NUMBER_SEPARATOR)
    scp_number = _extract_scp_number(word_list)
    if scp_number is not None:
        try:
                # int(scp_number) takes care if users already entered 001
                # because it makes it equal to 1
            formatted_number = _format_scp_number(int(scp_number))
            return _build_scp_url(formatted_number)
        except Exception:
            return None
    # @param word_list a list of strings
    # @return integer or None if error
def _extract_scp_number(word_list):
    captured_scp_number = None
    for index, word in enumerate(word_list):
        if word == "SCP":
                # We're gonna return the word after the current word (index+1)
                # But we have to make sure that the next word exists in the list
                # otherwise we will get IndexError exception
            if index + 1 < len(word_list):
                captured_scp_number = word_list[index + 1]
            else:
                return None
        # If we captured a string in the for loop we have to make sure that that
        # string is actually a number and not some random word example "SCP blabla"
    if captured_scp_number.isdigit():
        return captured_scp_number
    return None
    # Formats number as a string in format 001-MAXIMUM_SCP_NUMBER
    # This allows users to enter 1 instead of 001.
    #
    # @param number a positive integer to be formatted
    # @return string in format 001-MAXIMUM_SCP_NUMBER or raise Exception if error
def _format_scp_number(number):
    if number == 0:
        raise Exception("SCP 0 doesn't exist!")
    elif number > MAXIMUM_SCP_NUMBER:
        raise Exception("SCP number too high! Entry doesn't exist!")
    elif number < 10:
        return "00" + str(number)
    elif number < 100:
        return "0" + str(number)
    else:
        return str(number)
    # @param formatted_scp_number a string in format 001-MAXIMUM_SCP_NUMBER
    # @return string representing URL to SCP-number web page
def _build_scp_url(formatted_scp_number):
    base_url = "http://www.scp-wiki.net/scp-"
    prefix = "SCP-" + formatted_scp_number + ": "
    return prefix + base_url + formatted_scp_number
@client.event
async def on_message(message):
    if "SCP" in message.content:
        scp_link = get_scp_link(message.content)
        if scp_link is not None:
            await client.send_message(message.channel, scp_link)
#https://scp-wiki.net/scp-001
###########################################################################################################################
#and then the rest of this code is mine
#this \/ is the command code
quotes = [
    "Sorry, did I say something wrong? Pardon me for breathing which I never do anyway so I don't know why I bother to say it.",
    "I would correct your grammar as well, but you wouldn't listen. No one ever does...",
    "I'd make a suggestion, but you wouldn't listen. No one ever does."
    ]

@client.event
async def on_message(message):
    # We don't want the bot to reply to itself
    if message.author == client.user:
        return
    #or other bots
    if message.author.bot:
        return
    if message.content.startswith('m|bot'):
        msg = "Hi, I'm Marvin. I'm a bot that originated on r/scp and other SCP subreddits. I reply to people when i detect an SCP classification, such as SCP-280. I may not always be right."
        await client.send_message(message.channel, msg)
        print("[",time.strftime("%Y-%m-%d %H:%M:%S",ts),"]Someone used about.")
        
    if message.content.startswith('m|quote'):
        msg = "I wish i could tell you a quote, but my developer is so bad at what he does i can't."
        await client.send_message(message.channel, msg)
        print("[",time.strftime("%Y-%m-%d %H:%M:%S",ts),"]Someone used quote.")

    if message.content.startswith('m|getinvite'):
        msg = '{0.author.mention}, the invite code is https://discord.gg/WQJ7hRF'.format(message)
        await client.send_message(message.channel, msg)
        print("[",time.strftime("%Y-%m-%d %H:%M:%S",ts),"]Someone used getinvite.")
        
    if message.content.startswith('m|howto'):
        embed = discord.Embed(title="**How to use Marvin**", description="How Marvin will find any SCP for you", colour=discord.Colour(0x7a19fd))
        embed.set_author(name="Marvin")
        embed.set_footer(text="Marvin v1.1")
        embed.add_field(name="Main Use", value="For Marvin to find an SCP for you, say 'SCP-XXX' and replace the x's with any number 001-4999.", inline=False)
        embed.add_field(name="What doesn't work", value="Marvin can find you a lot of SCP's.. Except -J's. Also, be sure to use '001' or '037', not '1' or '37'.", inline=False)
        await client.send_message(message.channel, embed=embed)
        print("[",time.strftime("%Y-%m-%d %H:%M:%S",ts),"]Someone used howto.")

    if message.content.startswith('m|scp'):
        msg = 'The SCP Foundation is a secret organization entrusted by governments around the globe to contain and study anomalous individuals, entities, locations, objects, and phenomena operating outside the bounds of natural law. _Note: It is all entirely fictional. Any events that occur are purely coincidental._'
        await client.send_message(message.channel, msg)
        print("[",time.strftime("%Y-%m-%d %H:%M:%S",ts),"]Someone used about scp.")
    
    if message.content.startswith('m|cmds'):
            embed = discord.Embed(title="**List of commands**", description="List of commands to use.", colour=discord.Colour(0x7a19fd))
            embed.set_author(name="Marvin")
            embed.set_footer(text="Marvin v1.1")
            embed.add_field(name="m|bot", value="Bot info", inline=False)
            embed.add_field(name="m|scp", value="Info about the SCP Foundation", inline=False)
            embed.add_field(name="m|howto", value="How to use the main feature of this bot", inline=False)
            embed.add_field(name="m|getinvite", value="Invite to the bot support server", inline=False)
            embed.add_field(name="m|quote", value="Recite a quote.", inline=False)
            await client.send_message(message.channel, embed=embed)
            print("[",time.strftime("%Y-%m-%d %H:%M:%S",ts),"]Someone viewed the list of commands.")
@client.event
async def on_ready():
    print('------------------------------------------------')
    print('Logged in as:')
    print(client.user.name)
    print(client.user.id)
    print('------------------------------------------------')
    print("Marvin", version,"is connected and running!")
    print('------------------------------------------------')

client.run(TOKEN)
