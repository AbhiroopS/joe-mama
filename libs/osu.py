import requests, json, discord
from Token import osu


def osuuser(username):
    url = f'https://osu.ppy.sh/api/get_user?k={osu}&u={username}'
    response = requests.get(url, verify=True)
    data=response.json()
    embed = discord.Embed(
        colour=discord.Color.green(),
        title=(f'{data[0]["username"]}'),
        url=(f'https://osu.ppy.sh/users/{data[0]["user_id"]}')
    )
    embed.set_thumbnail(url=f'https://a.ppy.sh/{data[0]["user_id"]}')
    embed.add_field(name='Hit Accuracy', value=f'{data[0]["accuracy"][0:5]}%', inline=False)
    embed.add_field(name='Account Created on', value=f'{data[0]["join_date"]} UTC', inline=False)
    embed.add_field(name='Playcount', value=f'{data[0]["playcount"]}', inline=False)
    embed.add_field(name='Total PP', value=f'{data[0]["pp_raw"]}', inline=False)
    return embed