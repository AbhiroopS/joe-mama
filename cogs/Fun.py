import discord
import random
import os
from discord.ext import commands

class Fun(commands.Cog):

	def __init__(self,client):
		self.client=client

	@commands.Cog.listener()
	async def on_ready(self):
		print('Fun Module is online.')

	@commands.command(name='8ball',brief='Ask the Magical 8 Ball a question and get it answered.')
	async def _8ball(self,ctx,*,question):
		responses = ['It is certain.', 
				'It is decidedly so.', 
				'Without a doubt.', 
				'Yes - definitely.', 
				'You may rely on it.', 
				'As I see it, yes.', 
				'Most likely.', 
				'Outlook good.', 
				'Yes.', 
				'Signs point to yes.', 
				'Reply hazy, try again.', 
				'Ask again later.', 
				'Better not tell you now.', 
				'Cannot predict now.', 
				'Concentrate and ask again.', 
				"Don't count on it.", 
				'My reply is no.', 
				'My sources say no.', 
				'Outlook not so good.', 
				'Very doubtful.']
		await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')
		print('Executed 8Ball Command.\n')

def setup(client):
	client.add_cog(Fun(client))