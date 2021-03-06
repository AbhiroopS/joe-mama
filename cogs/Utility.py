import discord
import random
import os
import aiohttp, asyncio, async_timeout
import requests
import urllib.parse, urllib.request,re
import string
from bs4 import BeautifulSoup
from Config import prefix
from discord.ext import commands
from libs.anilist import animeSearch,mangaSearch
from libs.osu import osuuser
from Config import googleAPI

class Utility(commands.Cog):

    def __init__(self,client):
        self.client=client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Utility Module is online.')

    @commands.command(brief='Check the bots latency to discord.', usage=f'{prefix}ping')
    async def ping(self,ctx):
        embed=discord.Embed(
            description=f":ping_pong: {round(self.client.latency*1000)}ms",
            colour=2864934
        )
        await ctx.send(embed=embed)
        print('\nExecuted ping command.\n')

    @commands.command(brief='Get a link to invite this bot to a server.', usage=f'{prefix}invite')
    async def invite(self,ctx):
        embed = discord.Embed(
            colour=2864934,
            title="To invite me to your server, use this link",
            description=f"[Bot is currently not publically Available]\n\n Use `{prefix}help` to get a list of commands"
        )
        member=ctx.guild.get_member(self.client.user.id)
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)
        print('Executed invite command.\n')

    @commands.command(brief="Get the full size image of a user's avatar",aliases=["av"], usage=f'{prefix}avatar @SomeUser')
    async def avatar(self,ctx,member: discord.Member=None):
        member = ctx.author if not member else member
        embed = discord.Embed(
            colour=member.color, timestamp=ctx.message.created_at, title='Avatar URL', url=f'{member.avatar_url}')

        embed.set_image(url=member.avatar_url)
        embed.set_author(name=f'{member}')
        embed.set_footer(text=f'Requested by {ctx.author}')

        await ctx.send(embed=embed)
        print("Executed Avatar command.\n")

    @commands.command(brief='Get info about a user', aliases=["uinfo"], usage=f'{prefix}userinfo @SomeUser')
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
    
    @commands.command(brief='Get information about this server', aliases=["guild", "server"], usage=f'{prefix}serverinfo')
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

    @commands.command(aliases=['yt'], brief='Query for a youtube video', usage=f'{prefix}youtube [Search Query]')
    async def youtube(self, ctx, *, search):
        url=f'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&order=relevance&q={search}&key={googleAPI}'
        response = requests.get(url, verify=True)
        data=response.json()
        await ctx.send(f':mag: **| https://www.youtube.com/watch?v={data["items"][0]["id"]["videoId"]}**')

    @commands.command(brief="Search Anilist for an anime", aliases=["animu", "a"], usage=f'{prefix}anime [Search Query]')
    async def anime(self, ctx, *, title):
        embed = animeSearch(title)
        await ctx.send(embed=embed)

    @commands.command(brief="Search Anilist for a manga", aliases=["mango", "m"], usage=f'{prefix}manga [Search Query]')
    async def manga(self,ctx, *, title):
        embed = mangaSearch(title)
        await ctx.send(embed=embed)

    @commands.command(brief="Get info on an osu user", usage=f'{prefix}osu [osu Username]')
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
    
    @commands.command(brief="Get the Store Link for a Steam app", usage=f'{prefix}steam [Search Query]')
    async def steam(self, ctx, *, search_query):
            try:
                page = requests.get(f"https://store.steampowered.com/search/?term={search_query}", timeout=(3.05, 27))
                steampage = BeautifulSoup(page.content, 'html.parser')
                div = steampage.find("div", {"id": "search_resultsRows"})
                links = div.find_all('a', href=True)
                await ctx.send(links[0]['href'])
            except:
                await ctx.send("The requested search returned no results.")

def setup(client):
    client.add_cog(Utility(client))