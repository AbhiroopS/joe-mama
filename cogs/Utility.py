import discord
import random
import os
from discord.ext import commands

class Utility(commands.Cog):

	def __init__(self,client):
		self.client=client

	@commands.Cog.listener()
	async def on_ready(self):
		print('Utility Module is online.')

	@commands.command(brief='Check the bots latency to discord.')
	async def ping(self,ctx):
		embed=discord.Embed(
			description=f":ping_pong: {round(self.client.latency*1000)}ms",
		    colour=2864934
		)
		await ctx.send(embed=embed)
		print('Executed ping command.\n')

	@commands.command(brief='Get a link to invite this bot to a server.')
	async def invite(self,ctx):
		embed = discord.Embed(
			colour=2864934,
		    title="To invite me to your server, use this link",
			description="http://tiny.cc/Joe-Mama-Beta\n\n Use `>>help` to get a list of commands"
		)
		embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/654955750090866701/dd49fe7475433c1fb0ffa8a43dbd97fc.jpg?size=1024")
		await ctx.send(embed=embed)
		print('Executed invite command.\n')

	@commands.command(brief="Get the full size image of a user's avatar")
	async def avatar(self,ctx,member: discord.Member=None):
		member = ctx.author if not member else member
		embed = discord.Embed(
			colour=member.color, timestamp=ctx.message.created_at, title='Avatar URL', url=f'{member.avatar_url}')

		embed.set_image(url=member.avatar_url)
		embed.set_author(name=f'{member}')
		embed.set_footer(text=f'Requested by {ctx.author}')

		await ctx.send(embed=embed)
		print("Executed Avatar command.\n")

	@commands.command(brief='Get info about a user')
	async def userinfo(self,ctx,member: discord.Member=None):
		member=ctx.author if not member else member
		roles = [role for role in member.roles]
		embed = discord.Embed(
			colour=member.color, timestamp=ctx.message.created_at)

		embed.set_author(name=f'User info - {member}')
		embed.set_thumbnail(url=member.avatar_url)
		embed.set_footer(text=f'Requested by {ctx.author}')

		embed.add_field(name="ID:",value=member.id)
		embed.add_field(name="Guild Name:", value=member.display_name, inline=False)

		embed.add_field(name="Created at:", value=member.created_at.strftime("%a %#d %B %Y, %I:%M %p UTC"), inline=False)
		embed.add_field(name="Joined at:", value=member.joined_at.strftime("%a %#d %B %Y, %I:%M %p UTC"))

		embed.add_field(name=f'Roles ({len(roles)})', value=" ".join([role.mention for role in roles]), inline=False)
		embed.add_field(name="Top Role:", value=member.top_role.mention)

		embed.add_field(name="Bot?", value=member.bot, inline=False)

		await ctx.send(embed=embed)

def setup(client):
	client.add_cog(Utility(client))