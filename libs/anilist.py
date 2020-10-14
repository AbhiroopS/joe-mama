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
        studios
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
        averageScore
        favourites
        studios
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
            title=('{} ({}) {}'.format(result["data"]["Media"]["title"]["romaji"],
                                       result["data"]["Media"]["title"]["english"],
                                       result["data"]["Media"]["format"])),
            url=result["data"]["Media"]["siteUrl"],
            description=(removeTags(result["data"]["Media"]["description"])).replace("&quot;", '"')
        )
        embed.add_field(name="Status", value=result["data"]["Media"]["status"].upper(), inline=True)
        embed.add_field(name="Season",
                        value='{} {}'.format(result["data"]["Media"]["season"], result["data"]["Media"]["seasonYear"]),
                        inline=True)
        embed.add_field(name="Number of Episodes", value=result["data"]["Media"]["episodes"], inline=True)
        embed.add_field(name="Duration",
                        value='{} minutes/episode'.format(result["data"]["Media"]["duration"], inline=True))
        embed.add_field(name="Favourites", value=result["data"]["Media"]["favourites"], inline=True)
        embed.add_field(name="Average Score", value='{}%'.format(result["data"]["Media"]["averageScore"], inline=True))
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
            title=('{} ({}) {}'.format(result["data"]["Media"]["title"]["romaji"],
                                       result["data"]["Media"]["title"]["english"],
                                       result["data"]["Media"]["format"])),
            url=result["data"]["Media"]["siteUrl"],
            description=(removeTags(result["data"]["Media"]["description"])).replace("&quot;", '"')
        )

        embed.add_field(name="Status", value=result["data"]["Media"]["status"].upper(), inline=True)
        embed.add_field(name="Start Date",
                        value='{}/{}/{}'.format(result["data"]["Media"]["startDate"]["day"],
                                                result["data"]["Media"]["startDate"]["month"],
                                                result["data"]["Media"]["startDate"]["year"]),
                        inline=True)
        embed.add_field(name="Number of Chapters", value=replaceNone(result["data"]["Media"]["chapters"]), inline=True)
        embed.add_field(name="Number of Volumes", value=replaceNone(result["data"]["Media"]["volumes"]), inline=True)
        embed.add_field(name="Favourites", value=result["data"]["Media"]["favourites"], inline=True)
        embed.add_field(name="Average Score",
                        value='{}'.format(replaceNone(result["data"]["Media"]["averageScore"]), inline=True))
        embed.set_thumbnail(url=result["data"]["Media"]["coverImage"]["large"])
        return embed
