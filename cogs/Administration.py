import discord
import random
import os
from discord.ext import commands

class Administration(commands.Cog):

	def __init__(self,client):
		self.client=client

	@commands.Cog.listener()
	async def on_ready(self):
		print('Administration Module is online.')

	@commands.command(brief='Make the bot say something.')
	@commands.has_permissions(administrator=True)
	async def say(self,ctx,*, msg: str):
		await ctx.send(msg)

	@commands.command(brief='Kick an user from this server.')
	@commands.has_permissions(kick_members=True)
	async def kick(self,ctx,member:discord.Member,*,Reason=None):
		await member.kick(reason=Reason)
		await ctx.send(f'> {member} has been kicked from the Server.')

	@commands.command(brief='Ban an user from this server.')
	@commands.has_permissions(ban_members=True)
	async def ban(self,ctx,member:discord.Member,*,Reason=None):
		await member.ban(reason=Reason)
		await ctx.send(f'{member.mention} has been banned from the Server.')

	@commands.command(brief='Unban a banned user. Provide Name and Discriminator.')
	@commands.has_permissions(ban_members=True)
	async def unban(self,ctx,*,member):
		banned_users = await ctx.guild.bans()
		member_name,member_discriminator=member.split('#')
		for ban_entry in banned_users:
			user=ban_entry.user

			if(user.name, user.discriminator)==(member_name,member_discriminator):
				await ctx.guild.unban(user)
				await ctx.send(f'Unbanned {user.mention}')
				return

	@commands.command(brief='Delete a specifief amount of messages.')
	@commands.has_permissions(manage_messages=True)
	async def clear(self,ctx, amount:int):
		await ctx.channel.purge(limit=amount+1)
		await ctx.send(f'> {amount} messages have been deleted.')
		print(f'Cleared {amount} messages.\n')

def setup(client):
	client.add_cog(Administration(client))