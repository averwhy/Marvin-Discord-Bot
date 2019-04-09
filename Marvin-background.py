import discord
import asyncio

client = discord.Client()

async def my_background_task():
    await client.wait_until_ready()
    while True:
        #await client.change_presence(game=discord.Game(name='with m|cmds'))
        #await asyncio.sleep(10)
        await client.change_presence(game=discord.Game(name='with SCP-999'))
        await asyncio.sleep(10)
        await client.change_presence(game=discord.Game(name='with my devloper'))
        await asyncio.sleep(10)
        await client.change_presence(game=discord.Game(name='SCP Containment Breach'))
        await asyncio.sleep(10)
        await client.change_presence(game=discord.Game(name='with m|cmds'))
        await asyncio.sleep(10)
        await client.change_presence(game=discord.Game(name='[REDACTED]'))
        await asyncio.sleep(10)
        await client.change_presence(game=discord.Game(name='with m|howto'))
        await asyncio.sleep(10)
        
@client.event
async def on_ready():
    print('-----------------------------------------------------')
    print('Logged in as:')
    print(client.user.name)
    print(client.user.id)
    print('-----------------------------------------------------')
    print("Marvin is connected and running!")
    print("This feed is the background task one, not the main.")
    print('-----------------------------------------------------')

client.loop.create_task(my_background_task())
client.run('')
