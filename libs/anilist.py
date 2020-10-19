import discord
import requests

def SearchByID():
    query = '''
    query($id: Int, $type: MediaType) {
        Media(id: $id, type: $type) {
        title
        {
            romaji
            english
        }
        siteUrl
        type
        format
        genres
        status
        episodes
        duration
        status
        description(asHtml: true)
        coverImage {
            large
        }
        season
        seasonYear
        startDate {
            day
            month
            year
        }
        averageScore
        favourites
        studios(isMain: true)
        {
            edges
            {
                node
                {
                    name
                }
            }
        }
        chapters
        genres
        volumes
        hashtag
        }
        }
    '''
    return query

def SearchByTitle():
    query = '''
    query($search: String, $type: MediaType) {
        Media(search: $search, type: $type) {
        title
        {
            romaji
            english
        }
        siteUrl
        type
        format
        genres
        status
        episodes
        duration
        status
        description(asHtml: true)
        coverImage {
            large
        }
        season
        seasonYear
        startDate {
            day
            month
            year
        }
        endDate {
            day
            month
            year
        }
        averageScore
        favourites
        studios(isMain: true)
        {
            edges
            {
                node
                {
                    name
                }
            }
        }
        chapters
        volumes
        hashtag
        }
        }
    '''
    return query

def GetByID(type, id):
    type = type.upper()
    if type != 'ANIME' and type != 'MANGA':
        return False
    variables = {
        'type' : type,
        'id': id
    }
    return variables

def GetByTitle(type, title):
    type = type.upper()
    if type != 'ANIME' and type != 'MANGA':
        return False
    variables = {
        'type' : type,
        'search' : title
    }
    return variables

def run_query(query, variables):
    request = requests.post('https://graphql.anilist.co', json={'query': query, 'variables': variables})
    if request.status_code == 200:
        return request.json()
    elif request.status_code == 404:
        print ("Invalid search.")
        return
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

def removeTags(text):
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def cutLength(text):
    if len(text) > 900:
        return text[:900] + "..."
    return text

def replaceNone(text):
    if text is None:
        return 'N/A'
    return text

def formatconv(format):
    switcher = {
        "TV" : "TV",
        "TV_SHORT" : "TV Short",
        "MOVIE" : "Movie",
        "SPECIAL" : "Special",
        "OVA" : "OVA",
        "ONA" : "ONA",
        "MUSIC" : "Music",
        "MANGA" : "Manga",
        "NOVEL" : "Novel",
        "ONE_SHOT" : "One Shot"
    }
    return switcher.get(format, "N/A")

def statusconv(status):
    switcher = {
        "FINISHED": "Finished",
        "RELEASING": "Releasing",
        "NOT_YET_RELEASED": "Not Yet Released",
        "CANCELLED": "Cancelled"
    }
    return switcher.get(status, "N/A")       

def animeSearch(title):
    if title.isnumeric():
        query = SearchByID()
        variables = GetByID('anime', title)
    elif not title.isnumeric():
        query = SearchByTitle()
        variables = GetByTitle('anime', title)
    if variables:
        result = run_query(query, variables)
        if not result:
            return discord.Embed(description="There does not exist an anime with a title/ID of {}.".format(title))  

        embed = discord.Embed(
            colour=discord.Colour.blue(),
            title=('{}'.format(result["data"]["Media"]["title"]["romaji"])),
            url=result["data"]["Media"]["siteUrl"],
            description=(removeTags(result["data"]["Media"]["description"])).replace("&quot;", '"')
        )
        embed.add_field(name="Type", value=formatconv(result["data"]["Media"]["format"]), inline=True)
        embed.add_field(name="Status", value=statusconv(result["data"]["Media"]["status"]), inline=True)
        embed.add_field(name="Season",
                        value='{} {}'.format(result["data"]["Media"]["season"].capitalize(), result["data"]["Media"]["seasonYear"]),
                        inline=True)
        if result["data"]["Media"]['startDate']['day']:
            embed.add_field(name='Start date',
                            value='%s/%s/%s' % (result["data"]["Media"]['startDate']['day'],
                                                result["data"]["Media"]['startDate']['month'],
                                                result["data"]["Media"]['startDate']['year']),
                            inline=True)
        else:
            embed.add_field(name='Start date', value='-', inline=True)

        if result["data"]["Media"]['endDate']['day']:
            embed.add_field(name='End date',
                            value='%s/%s/%s' % (result["data"]["Media"]['endDate']['day'],
                                                result["data"]["Media"]['endDate']['month'],
                                                result["data"]["Media"]['endDate']['year']),
                            inline=True)
        else:
            embed.add_field(name='End date', value='-', inline=True)
        
        embed.add_field(name="Episodes", value=result["data"]["Media"]["episodes"], inline=True)
        embed.add_field(name="Duration",
                        value='{} minutes/episode'.format(result["data"]["Media"]["duration"], inline=True))

        if result["data"]["Media"]["studios"]["edges"][0]["node"]["name"]:
            embed.add_field(name='Studio',
                            value=result["data"]["Media"]["studios"]["edges"][0]["node"]["name"],
                            inline=True)
        else:
            embed.add_field(name='Studio', value='-', inline=True)
        
        embed.add_field(name="Favourites", value=result["data"]["Media"]["favourites"], inline=True)
        embed.add_field(name="Average Score", value='{}%'.format(result["data"]["Media"]["averageScore"], inline=True))
        embed.add_field(name='Genres', value=', '.join(result["data"]["Media"]['genres']), inline=True)
        embed.set_thumbnail(url=result["data"]["Media"]["coverImage"]["large"])
        return embed

def mangaSearch(title):
    if title.isnumeric():
        query = SearchByID()
        variables = GetByID('manga', title)

    elif not title.isnumeric():
        query = SearchByTitle()
        variables = GetByTitle('manga', title)

    if variables:
        result = run_query(query, variables)

        if not result:
            return discord.Embed(description="There does not exist a manga with a title/ID of {}.".format(title))

        embed = discord.Embed(
            colour=discord.Colour.blue(),
            title=('{}'.format(result["data"]["Media"]["title"]["romaji"])),
            url=result["data"]["Media"]["siteUrl"],
            description=(removeTags(result["data"]["Media"]["description"])).replace("&quot;", '"')
        )
        
        embed.add_field(name="Type", value=formatconv(result["data"]["Media"]["format"]), inline=True)
        embed.add_field(name="Status", value=statusconv(result["data"]["Media"]["status"]), inline=True)

        if result["data"]["Media"]['startDate']['day']:
            embed.add_field(name='Start date',
                            value='%s/%s/%s' % (result["data"]["Media"]['startDate']['day'],
                                                result["data"]["Media"]['startDate']['month'],
                                                result["data"]["Media"]['startDate']['year']),
                            inline=True)
        else:
            embed.add_field(name='Start date', value='-', inline=True)

        if result["data"]["Media"]['endDate']['day']:
            embed.add_field(name='End date',
                            value='%s/%s/%s' % (result["data"]["Media"]['endDate']['day'],
                                                result["data"]["Media"]['endDate']['month'],
                                                result["data"]["Media"]['endDate']['year']),
                            inline=True)
        else:
            embed.add_field(name='End date', value='-', inline=True)
            
        embed.add_field(name="Chapters", value=replaceNone(result["data"]["Media"]["chapters"]), inline=True)
        embed.add_field(name="Volumes", value=replaceNone(result["data"]["Media"]["volumes"]), inline=True)
        embed.add_field(name="Favourites", value=result["data"]["Media"]["favourites"], inline=True)
        embed.add_field(name="Average Score",
                        value='{}'.format(replaceNone(result["data"]["Media"]["averageScore"]), inline=True))
        embed.add_field(name='Genres', value=', '.join(result["data"]["Media"]['genres']), inline=True)
        embed.set_thumbnail(url=result["data"]["Media"]["coverImage"]["large"])
        return embed
