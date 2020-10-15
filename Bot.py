import discord
import os
import asyncio
from discord.ext import commands, tasks
from itertools import cycle

# discord.py version = 1.4.1

TOKEN=open("Token.txt","r").read()
client = commands.Bot(command_prefix='>>')
status = cycle(['With deez nuts','with yo mama'])

client.remove_command('help')

@client.event
async def on_ready():
	change_status.start()
	print('Bot is ready.\n')

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
	print(f'{extension} has been reloaded\n')

for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f'cogs.{filename[:-3]}')

@client.command()
async def help(ctx):
	pages = 3
	cur_page = 1

	embed1=discord.Embed(color=ctx.author.color)
	embed1.set_author(name="Help",icon_url="https://clipartstation.com/wp-content/uploads/2018/09/clipart-question-mark-1-1.jpg")
	embed1.set_footer(text=f'Page 1/{pages} - Requested by {ctx.author}')
	embed1.add_field(name="help", value="Show this message",inline=False)
	embed1.add_field(name="ban <member>",value="Ban a user",inline=False)
	embed1.add_field(name="kick <member>", value="Kick a user",inline=False)
	embed1.add_field(name="clear <x>", value="Delete last x messages",inline=False)
	embed1.add_field(name="unban <member#0000>", value="Unban an user, provide name and discriminator",inline=False)
	embed1.add_field(name="say <text>", value="Make the bot say something",inline=False)

	embed2=discord.Embed(color=ctx.author.color)
	embed2.set_author(name="Help",icon_url="https://clipartstation.com/wp-content/uploads/2018/09/clipart-question-mark-1-1.jpg")
	embed2.set_footer(text=f'Page 2/{pages} - Requested by {ctx.author}')
	embed2.add_field(name="8ball <question>", value="Ask the Magical 8 Ball a question and get it answerered",inline=False)
	embed2.add_field(name="invite", value="Get a link to invite this bot to your server",inline=False)
	embed2.add_field(name="ping", value="Check the bot's latency to discord",inline=False)
	embed2.add_field(name="youtube <search term>", value="Search youtube", inline=False)
	embed2.add_field(name="userinfo <member>", value="Get information on a user",inline=False)
	embed2.add_field(name="avatar <member>", value="Get the full size Avatar of a user with its URL", inline=False)

	embed3=discord.Embed(color=ctx.author.color)
	embed3.set_author(name="Help",icon_url="https://clipartstation.com/wp-content/uploads/2018/09/clipart-question-mark-1-1.jpg")
	embed3.set_footer(text=f'Page 3/{pages} - Requested by {ctx.author}')
	embed3.add_field(name="anime <search query>", value="Search for an Anime on Anlist",inline=False)
	embed3.add_field(name="manga <search query>", value="Search for a Manga on Anilist",inline=False)
	embed3.add_field(name="vcmute", value="Mute everyone in your voice channel", inline=False)
	embed3.add_field(name="vcunmute", value="Unmute everyone in your voice channel", inline=False)
	
	contents = [ embed1 , embed2, embed3 ]
	message = await ctx.send(embed=contents[cur_page-1])

	await message.add_reaction("◀️")
	await message.add_reaction("▶️")

	def check(reaction, user):
		return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]

	while True:
		try:
			reaction, user = await client.wait_for("reaction_add", timeout=60, check=check)

			if str(reaction.emoji) == "▶️" and cur_page != pages:
				cur_page += 1
				await message.edit(embed=contents[cur_page-1])
				await message.remove_reaction(reaction, user)

			elif str(reaction.emoji) == "◀️" and cur_page > 1:
				cur_page -= 1
				await message.edit(embed=contents[cur_page-1])
				await message.remove_reaction(reaction, user)

			else:
				await message.remove_reaction(reaction, user)
		except asyncio.TimeoutError:
			await message.delete()
			break

client.run(TOKEN)