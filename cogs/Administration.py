import discord
import random
import os
from discord import Embed
from discord.ext import commands

class Administration(commands.Cog):

    def __init__(self,client):
        self.client=client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Administration Module is online.')

    @commands.command(brief='Make the bot say something.')
    @commands.has_guild_permissions(administrator=True)
    async def say(self,ctx,*, msg: str):
        embed=discord.Embed(
            description=f'{msg}',
            color=2864934
        )
        await ctx.send(embed=embed)

    @commands.command(brief='Kick an user from this server.')
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self,ctx,member:discord.Member,*,Reason=None):
        await member.kick(reason=Reason)
        embed = discord.Embed(
            description=f'{member} has been kicked from the server.\n\n Reason:`{Reason}`',
            color=2864934
        )
        await ctx.send(embed=embed)

    @commands.command(brief='Ban an user from this server.')
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self,ctx,member:discord.Member,*,Reason=None):
        await member.ban(reason=Reason)
        embed = discord.Embed(
            description=f'{member} has been banned from the server.\n\n Reason:`{Reason}`',
            color=2864934
        )
        await ctx.send(embed=embed)

    @commands.command(brief='Unban a banned user. Provide Name and Discriminator.')
    @commands.has_guild_permissions(ban_members=True)
    async def unban(self,ctx,*,member):
        banned_users = await ctx.guild.bans()
        member_name,member_discriminator=member.split('#')
        embed = discord.Embed(
            description=f'{member} is no longer banned.',
            color=2864934
        )
        embed2 = discord.Embed(
            description=f'{member} could not be found on list of banned users.',
            color=2864934
        )
        await ctx.send(embed=embed)
        for ban_entry in banned_users:
            user=ban_entry.user
            if(user.name, user.discriminator)==(member_name,member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(embed=embed)
                return
            else:
                await ctx.send(embed=embed2)
                return

    @commands.command(brief='Delete a specified amount of messages.')
    @commands.has_guild_permissions(manage_messages=True)
    async def clear(self,ctx, amount:int):
        await ctx.channel.purge(limit=amount+1)
        embed = discord.Embed(
            description=f'{amount} messages have been deleted.',
            color=2864934
        )
        await ctx.send(embed=embed)
        print(f'Cleared {amount} messages.\n')
    
    @commands.command()
    @commands.has_guild_permissions(mute_members=True)
    async def vcmute(self,ctx):
        vc = ctx.author.voice.channel
        for member in vc.members:
            await member.edit(mute=True)
    
    @commands.command()
    @commands.has_guild_permissions(mute_members=True)
    async def vcunmute(self,ctx):
        vc = ctx.author.voice.channel
        for member in vc.members:
            await member.edit(mute=False)

def setup(client):
    client.add_cog(Administration(client))