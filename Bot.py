import discord
import os
from discord.ext import commands, tasks
from itertools import cycle

client = commands.Bot(command_prefix='>>')
status = cycle(['With deez nuts','Ligma Ballz', 'Sugondese'])

@client.event
async def on_ready():
	change_status.start()
	print('Bot is ready.')

@tasks.loop(seconds=600)
async def change_status():
	await client.change_presence(activity=discord.Game(next(status)))

@client.event
async def on_member_join(member):
	print(f'{member} has joined the server.')

@client.event
async def on_member_remove(member):
	print(f'{member} has left the server.')

def is_it_me(ctx):
	return ctx.author.id == 173484983036542976

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

for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f'cogs.{filename[:-3]}')

client.run('NjU0OTU1NzUwMDkwODY2NzAx.XfNFGw.la2uIOAsAoxn96FiC-BPBAzj_KA')