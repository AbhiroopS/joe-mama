import discord
import random
import os
import requests
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
        embed = discord.Embed(
            colour=2864934
        )
        embed.add_field(name=f":question: Question", value=f"{question}", inline="false")
        embed.add_field(name=f":8ball: Answer", value=f"{random.choice(responses)}")
        await ctx.send(embed=embed)
        print('Executed 8Ball Command.\n')
    
    @commands.command(aliases=["meow"])
    async def cat(self, ctx):
        url="http://aws.random.cat/meow"
        response = requests.get(url)
        data=response.json()
        await ctx.send(f'{data["file"]}')

    @commands.command(aliases=["woof"])
    async def dog(self, ctx):
        url="https://random.dog/woof.json"
        response = requests.get(url)
        data=response.json()
        await ctx.send(f'{data["url"]}')

def setup(client):
    client.add_cog(Fun(client))