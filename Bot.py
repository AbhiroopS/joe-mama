import asyncio
import os
from itertools import cycle

import discord
from discord.ext import commands, tasks

from Config import discordtoken,Owner,prefix

# discord.py version = 1.5.0

client = commands.Bot(command_prefix=prefix)
status = f'{prefix}help'

client.remove_command('help')

@client.event
async def on_ready():
    # change_status.start()
    print('Bot is ready.\n')

# @tasks.loop(seconds=600)
# async def change_status():
#     await client.change_presence(activity=discord.Game(next(status)))

@client.event
async def on_member_join(member):
    print(f'{member} has joined the server.')

@client.event
async def on_member_remove(member):
    print(f'{member} has left the server.')

def is_it_me(ctx):
    return ctx.author.id == int(Owner)

@client.command(hidden=True)
@commands.check(is_it_me)
async def load(ctx,extension):
    client.load_extension(f'cogs.{extension}')

@client.command(hidden=True)
@commands.check(is_it_me)
async def unload(ctx,extension):
    client.unload_extension(f'cogs.{extension}')

@client.command(hidden=True)
@commands.check(is_it_me)
async def reload(ctx,extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    print(f'{extension} has been reloaded\n')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.command()
async def help(ctx):

    def aliasprint(aliases):
        if not aliases:
            return ""
        else:
            ali="/"
            ali+='/'.join(aliases)
            return ali
    
    Home=discord.Embed(color=ctx.author.color,
    description=f"An open source multipurpose discord bot written in python by Abhiroop#7339\n\n**Click on the given reactions to view commands relevant to the following categories:**\n\n 🏠 : View this Page\n🎱 : Fun and Games\n🔍 : Utility\n🛠️ : Administration\n"
    )
    Home.set_author(name="Help Menu", icon_url="https://clipartstation.com/wp-content/uploads/2018/09/clipart-question-mark-1-1.jpg")
    Home.set_footer(text=f'Requested by {ctx.author}')
    Home.add_field(name="Bot Prefix", value=f'`{prefix}`', inline=False)
    Home.add_field(name="Source Code", value=f'https://github.com/AbhiroopS/joe-mama')

    Fun=discord.Embed(color=ctx.author.color)
    Fun.set_author(name="Fun", icon_url="https://clipartstation.com/wp-content/uploads/2018/09/clipart-question-mark-1-1.jpg")
    Fun.set_footer(text=f'Requested by {ctx.author}')
    cogobj = client.get_cog('Fun')
    commands = cogobj.get_commands()
    for command in commands:
        Fun.add_field(name=f'{command}{aliasprint(command.aliases)}', value=f'{command.brief}\nUsage:`{command.usage}`\n', inline=False)

    Util=discord.Embed(color=ctx.author.color)
    Util.set_author(name="Utility", icon_url="https://clipartstation.com/wp-content/uploads/2018/09/clipart-question-mark-1-1.jpg")
    Util.set_footer(text=f'Requested by {ctx.author}')
    cogobj = client.get_cog('Utility')
    commands = cogobj.get_commands()
    for command in commands:
        Util.add_field(name=f'{command}{aliasprint(command.aliases)}', value=f'{command.brief}\nUsage:`{command.usage}`\n', inline=False)

    Admin=discord.Embed(color=ctx.author.color)
    Admin.set_author(name="Administration", icon_url="https://clipartstation.com/wp-content/uploads/2018/09/clipart-question-mark-1-1.jpg")
    Admin.set_footer(text=f'Requested by {ctx.author}')
    cogobj = client.get_cog('Administration')
    commands = cogobj.get_commands()
    for command in commands:
        Admin.add_field(name=f'{command}{aliasprint(command.aliases)}', value=f'{command.brief}\nUsage:`{command.usage}`\n', inline=False)

    contents = [ Home, Fun, Util, Admin]
    message = await ctx.send(embed=contents[0])

    emojis=["🏠","🎱","🔍","🛠️"]
    for emoji in emojis:
        await message.add_reaction(emoji)

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["🏠", "🎱","🔍","🛠️"]

    while True:
        try:
            reaction, user = await client.wait_for("reaction_add", timeout=60, check=check)

            if str(reaction.emoji) == "🏠":
                await message.edit(embed=contents[0])
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == "🎱":
                await message.edit(embed=contents[1])
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == "🔍":
                await message.edit(embed=contents[2])
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == "🛠️":
                await message.edit(embed=contents[3])
                await message.remove_reaction(reaction, user)

            else:
                await message.remove_reaction(reaction, user)

        except asyncio.TimeoutError:
            await message.delete()
            break

client.run(discordtoken)
