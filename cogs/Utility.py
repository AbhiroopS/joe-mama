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
		await ctx.send(f':ping_pong: Pong! {round(self.client.latency*1000)}ms')
		print('Executed ping command.\n')

	@commands.command(brief='Get a link to invite this bot to a server.')
	async def invite(self,ctx):
		await ctx.send('> Use the following link to invite this bot to your server:')
		await ctx.send('> https://discordapp.com/api/oauth2/authorize?client_id=654955750090866701&permissions=8&scope=bot')
		print('Executed invite command.\n')

def setup(client):
	client.add_cog(Utility(client))