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

def setup(client):
	client.add_cog(Utility(client))