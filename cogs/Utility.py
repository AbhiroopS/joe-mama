import discord
import random
import os
import aiohttp, asyncio, async_timeout
from discord.ext import commands
import urllib.parse, urllib.request,re
from libs.anilist import animeSearch,mangaSearch
from libs.osu import osuuser
from Token import googleAPI
import requests

class Utility(commands.Cog):

    def __init__(self,client):
        self.client=client
    
    async def gametoid(self, gamename):
        """Convert a game name to its ID"""
        session = aiohttp.ClientSession()

        async with session.get("http://api.steampowered.com/ISteamApps/GetAppList/v2") as r:
            response = await r.json()
        response = response['applist']['apps']
        try:
            gameid = next((item for item in response if item["name"] == gamename))
        except StopIteration:
            session.close()
            return False
        gameid = gameid['appid']
        await session.close()
        return gameid

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
        print('\nExecuted ping command.\n')

    @commands.command(brief='Get a link to invite this bot to a server.')
    async def invite(self,ctx):
        embed = discord.Embed(
            colour=2864934,
            title="To invite me to your server, use this link",
            description="Not a Public Bot\n\n Use `>>help` to get a list of commands"
        )
        member=ctx.guild.get_member(self.client.user.id)
        embed.set_thumbnail(url=member.avatar_url)
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
    
    @commands.command(aliases=["guild", "server"])
    async def serverinfo(self, ctx, guild: discord.guild = None):
        guild=ctx.guild if not guild else guild
        embed = discord.Embed(title=ctx.guild.name, colour=ctx.author.color, timestamp=ctx.message.created_at)
        embed.set_thumbnail(url=ctx.guild.icon_url_as(size=2048))
        embed.set_footer(text=f'Requested by {ctx.author}')
        embed.add_field(name="ID", value=ctx.guild.id)
        embed.add_field(name="Owner", value=ctx.guild.owner.mention, inline=False)
        embed.add_field(name="Region", value=ctx.guild.region, inline=False)
        embed.add_field(name="Members", value=str(ctx.guild.member_count), inline=False)
        embed.add_field(name="Text channels", value=str(len(ctx.guild.text_channels)), inline=False)
        embed.add_field(name="Voice channels", value=str(len(ctx.guild.voice_channels)), inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=['yt'], brief='Query for a youtube video')
    async def youtube(self, ctx, *, search):
        url=f'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&order=relevance&q={search}&key={googleAPI}'
        response = requests.get(url, verify=True)
        data=response.json()
        await ctx.send(f':mag: **| https://www.youtube.com/watch?v={data["items"][0]["id"]["videoId"]}**')

    @commands.command(aliases=["animu", "a"])
    async def anime(self, ctx, *, title):
        embed = animeSearch(title)
        await ctx.send(embed=embed)

    @commands.command(aliases=["mango", "m"])
    async def manga(self,ctx, *, title):
        embed = mangaSearch(title)
        await ctx.send(embed=embed)

    @commands.command(brief="Get info on an osu user")
    async def osu(self, ctx, *, username=None):
        if username==None:
            embed = discord.Embed(
                colour=discord.Color.red(),
                description="Please provide a Username"
            )
            await ctx.send(embed=embed)
        else:
            embed = osuuser(username)
            embed.set_footer(text=f'Requested by {ctx.author}')
            await ctx.send(embed=embed)
    
    @commands.command(brief="Get the Store Link for a Steam app")
    async def steam(self, ctx, *, gamename):
            gameid=await self.gametoid(gamename)
            if gameid==False:
                await ctx.send("Game not Found")
            else:
                await ctx.send(f'https://store.steampowered.com/app/{gameid}/')

def setup(client):
    client.add_cog(Utility(client))