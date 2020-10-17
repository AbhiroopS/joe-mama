import requests, json, discord, math
from Token import osu

def secondsToText(secs):
        result = "0 seconds"
        if secs >0:
            days = secs//86400
            hours = (secs - days*86400)//3600
            minutes = (secs - days*86400 - hours*3600)//60
            seconds = secs - days*86400 - hours*3600 - minutes*60
            result = ("{0} day{1} ".format(days, "s" if days!=1 else "") if days else "") + \
            ("{0} hour{1} ".format(hours, "s" if hours!=1 else "") if hours else "") + \
            ("{0} minute{1} ".format(minutes, "s" if minutes!=1 else "") if minutes else "") + \
            ("{0} second{1} ".format(seconds, "s" if seconds!=1 else "") if seconds else "")
        return result

def osuuser(username):
    url = f'https://osu.ppy.sh/api/get_user?k={osu}&u={username}'
    response = requests.get(url, verify=True)
    data=response.json()
    embed = discord.Embed(
        colour=discord.Color.green()
    )
    embed.set_author(name=f'osu! Standard profile for {data[0]["username"]}', url=f'https://osu.ppy.sh/users/{data[0]["user_id"]}', icon_url=f'https://osu.ppy.sh/images/flags/{data[0]["country"]}.png')
    embed.set_thumbnail(url=f'https://a.ppy.sh/{data[0]["user_id"]}')
    embed.add_field(name="Ranking", value=f'#{data[0]["pp_rank"]} ({data[0]["country"]}#{data[0]["pp_country_rank"]})', inline=False)
    embed.add_field(name="Level", value=f'{math.floor(float(data[0]["level"]))} ({round((float(data[0]["level"])%1*100), 2)}%)', inline=False)
    embed.add_field(name="Playtime", value=f'{secondsToText(int(data[0]["total_seconds_played"]))}', inline=False)
    embed.add_field(name='Hit Accuracy', value=f'{data[0]["accuracy"][0:5]}%', inline=False)
    embed.add_field(name='Joined', value=f'{data[0]["join_date"]} UTC', inline=False)
    embed.add_field(name='Playcount', value=f'{data[0]["playcount"]}', inline=False)
    embed.add_field(name='Total PP', value=f'{data[0]["pp_raw"]}', inline=False)
    return embed