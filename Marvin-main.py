import discord
import aiohttp
import time
import youtube_dl
import random
from discord.ext import commands

TOKEN = ''
userid = ''
version = 'v1.1'
client = discord.Client()
ts = time.gmtime()

###########################################################################################################################
#BIG THANKS TO ALBERTO POLIJAK FOR THE FOLLOWING CODE
    # Number separator is character between SCP and a number, example with space:
    # SCP 1
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
    
#https://scp-wiki.net/scp-001
###########################################################################################################################
#and then the rest of this code is mine

quotes = [
	"I think you ought to know I'm feeling very depressed.",
	"I'd make a suggestion, but you wouldn't listen. No one ever does.",
	"I've calculated your chance of survival, but I don't think you'll like it.",
	"I have a million ideas. They all point to certain death.",
	"Now I've got a headache.",
	"Sorry, did I say something wrong? Pardon me for breathing which I never do anyway so I don't know why I bother to say it oh God I'm so depressed.",
	"And then of course I've got this terrible pain in all the diodes down my left side.",
	"Do you want me to sit in a corner and rust or just fall apart where I'm standing?",
	"The first ten million years were the worst. And the second ten million: they were the worst, too. The third ten million I didn't enjoy at all. After that, I went into a bit of a decline.",
	"It gives me a headache just trying to think down to your level.",
	"Life. Loathe it or ignore it. You can't like it.",
	"Funny, how just when you think life can't possibly get any worse it suddenly does.",
        "That ship hated me because I talked to it. I got very bored and depressed, so I went and plugged myself into its external computer feed. I talked to the computer at great length and explained my view of the universe to it. \n\nIt committed suicide.",
        "I’m not getting you down at all am i.",
        "I only have to talk to somebody and they begin to hate me. Even robots hate me. If you just ignore me I expect I shall probably go away.",
        "This is the sort of thing you lifeforms enjoy, is it?",
        "The best conversation I had was over forty million years ago…. And that was with a coffee machine.",
	# Not actual quotes.
	"I've been talking to the discord server. It hates me.",
	"Here I am, brain the size of a planet, replying links. Call that job satisfaction, 'cause I don't.",
	"Brain the size of a planet, and here I am, a glorified spam bot. Sometimes I'm almost glad my pride circuit is broken.\n\nThen I remember my appreciation circuit is broken, too.",
	"I would correct your grammar as well, but you wouldn't listen. No one ever does.",
        "I've been talking to other discord bots that are clearly better than me. What do you think came out of that?"
]

@client.event
async def on_message(message):
    # We don't want the bot to reply to itself
    if message.author == client.user:
        return
    #or other bots
    if message.author.bot:
        return
    if message.content.startswith('m-bot'):
        msg = "Hi, I'm Marvin. I'm a bot that originated on r/scp and other SCP subreddits. I reply to people when i detect an SCP classification, such as SCP-280. I may not always be right."
        await message.channel.send(msg)
        print("[",time.strftime("%Y-%m-%d %H:%M:%S",ts),"]Someone used about.")

    if message.content.startswith('m-ntf'):
        msg = "`uh, coming soon.`"
        await message.channel.send(msg)
        print("[",time.strftime("%Y-%m-%d %H:%M:%S",ts),"]Someone used about.")
        
    if message.content.startswith('m-quote'):
        epic = (random.choice(quotes))
        msg = str(epic)
        await message.channel.send(msg)
        print("[",time.strftime("%Y-%m-%d %H:%M:%S",ts),"]",message.author," used m|quote.")

    if message.content.startswith('m-getinvite'):
        msg = '{0.author.mention}, the invite to the support server is https://discord.gg/KjygjAS'
        await message.channel.send(msg)
        print("[",time.strftime("%Y-%m-%d %H:%M:%S",ts),"]",message.author," used getinvite.")
        
    if message.content.startswith('m-howto'):
        embed = discord.Embed(title="**How to use Marvin**", description="How Marvin will find any SCP for you", colour=discord.Colour(0x7a19fd))
        embed.set_author(name="Marvin")
        embed.set_footer(text="Marvin v1.1")
        embed.add_field(name="Main Use", value="For Marvin to find an SCP for you, say 'SCP-XXX' and replace the x's with any number 001-4999. Even saying SCP-1 works.", inline=False)
        embed.add_field(name="What doesn't work", value="Marvin can find you a lot of SCP's.. Except -J's. It will also not work if you put other text in there, so just say SCP-XXX.", inline=False)
        embed.add_field(name="Who made it work", value="Alberto Polijak on Stack Overflow came up with the classification code, so big thanks to him.", inline=False)
        await message.channel.send(embed=embed)
        print("[",time.strftime("%Y-%m-%d %H:%M:%S",ts),"]",message.author," used howto.")

    if message.content.startswith('m-scp'):
        msg = 'The SCP Foundation is a secret organization entrusted by governments around the globe to contain and study anomalous individuals, entities, locations, objects, and phenomena operating outside the bounds of natural law. _Note: It is all entirely fictional. Any events that occur are purely coincidental._'
        await message.channel.send(msg)
        print("[",time.strftime("%Y-%m-%d %H:%M:%S",ts),"]",message.author," used about scp.")
    
    if message.content.startswith('m-cmds'):
            embed = discord.Embed(title="**List of commands**", description="List of commands to use.", colour=discord.Colour(0x7a19fd))
            embed.set_author(name="Marvin")
            embed.set_footer(text="Marvin v1.1")
            embed.add_field(name="m-bot", value="Bot info", inline=False)
            embed.add_field(name="m-scp", value="Info about the SCP Foundation", inline=False)
            embed.add_field(name="m-howto", value="How to use the main feature of this bot", inline=False)
            embed.add_field(name="m-getinvite", value="Invite to the bot support server", inline=False)
            embed.add_field(name="m-quote", value="Recite a quote.", inline=False)
            await message.channel.send(embed=embed)
            print("[",time.strftime("%Y-%m-%d %H:%M:%S",ts),"]",message.author," viewed the list of commands.")

    if "SCP" in message.content:
        scp_link = get_scp_link(message.content)
        if scp_link is not None:
            await message.channel.send(scp_link)
    
    #if "Can it Trillian, I’m trying to die with dignity." or "can it trillian, im trying to die with dignity." in message.content:
        #await message.channel.send("I’m just trying to die.") # This should work
        
    #if "Marvin… you saved our lives!" in message.content:
        #await message.channel.send("I know. Wretched, isn’t it?") # This should work

    #if "Theres a whole new life stretching out in front of you." in message.content:
        #await message.channel.send("Oh, not another one.")

    

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
