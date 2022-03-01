import discord
import requests
import json
import random
import youtube_dl
import os
import validators
import urllib.request as u
from requests import get
from GrabzIt import GrabzItImageOptions, GrabzItClient
from yelp.client import Client
from riotwatcher import LolWatcher
# import urllib.request as u
# from keep_alive import keep_alive


bold_text = '\033[1m'
ydl_opts = {'format': 'bestaudio/best',
            'postprocesors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
                    }],
            }


def spongegar(text):
    updated_text = []
    for character in text:
        r = random.randint(0, 1)

        if r:
            updated_text.append(character.upper())
        else:
            updated_text.append(character.lower())
    return ''.join(updated_text)


def get_inspirational_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']

    return quote


def screenshot_website(question):
    # req = u.Request(question, headers={'User-Agent': 'Mozilla/5.0'})
    # page = u.urlopen(req)

    for file in os.listdir("./"):
        if file == "pic.jpg":
            os.remove(file)

    g = GrabzItClient.GrabzItClient("YOUR_API_KEY_1=",
                                    "YOUR_API_KEY_2=")
    options = GrabzItImageOptions.GrabzItImageOptions()
    options.format = "jpg"

    # capture full length of webpage
    options.browserHeight = -1
    options.width = -1
    options.height = -1

    # save url type as an image
    g.URLToImage(question, options)
    g.SaveTo("pic.jpg")


def get_yelp_results(item, location):
    api_key = "YOUR_API_KEY"
    headers = {'Authorization': 'Bearer %s' % api_key}
    Client(api_key)

    url = 'https://api.yelp.com/v3/businesses/search'

    params = {'term': item, 'location': location}

    req = requests.get(url, params, headers=headers)
    # print('The status code is {}'.format(req.status_code))
    results_txt = req.text

    parsed = json.loads(results_txt)
    # print(json.dumps(parsed, indent=4))

    businesses = parsed["businesses"]
    results = ""
    counter = 0

    for business in businesses:
        if counter == 5:
            return results

        results += f"Name: {business['name']}"
        results += f"\nRating: {business['rating']}/5.0"
        results += f"\nAddress: {' '.join(business['location']['display_address'])}"
        results += f"\nPhone: {business['phone']}"

        shortened_url = ""
        for c in business['url']:
            if c == "?":
                break
            shortened_url += c

        results += f"\nURL: {shortened_url}"
        results += "\n\n"
        counter += 1


def get_reddit_meme():
    response = requests.get("https://meme-api.herokuapp.com/gimme")
    json_data = json.loads(response.text)

    u.urlretrieve(json_data['url'], "meme.png")


def get_lol_stats(summoner_name):
    summoner_stats = ""
    watcher = LolWatcher("YOUR_API_KEY")
    summoner = watcher.summoner.by_name("na1", summoner_name)
    summoner_stats += f"{summoner['name']} (Level {summoner['summonerLevel']})\n"

    ranked_stats = watcher.league.by_summoner("na1", summoner['id'])

    ranked_record = ""

    for i in range(0, 2):
        for key in ranked_stats[i]:
            if key == 'queueType':
                summoner_stats += f"{ranked_stats[i][key]}: "
            if key == 'tier' or key == 'rank':
                summoner_stats += f"{ranked_stats[i][key]} "
            if key == 'wins':
                ranked_record += f"\nW/L Ratio: {str(ranked_stats[i][key])}"
            if key == 'losses':
                ranked_record += f"-{str(ranked_stats[i][key])}\n\n"
        summoner_stats += ranked_record
        ranked_record = ""

    champion_dict = {}
    latest = watcher.data_dragon.versions_for_region("na1")['n']['champion']
    champion_list = watcher.data_dragon.champions(latest, False, "en_US")
    for key in champion_list['data']:
        row = champion_list['data'][key]
        champion_dict[row['key']] = row['id']

    champion_masteries = watcher.champion_mastery.by_summoner("na1", summoner['id'])
    top_5_champion_masteries = {}

    for i in range(0, len(champion_masteries)):
        if len(top_5_champion_masteries) == 5:
            break
        top_5_champion_masteries[champion_masteries[i]['championPoints']] = str(champion_masteries[i]['championId'])

    for key in top_5_champion_masteries:
        for value in champion_dict:
            if value == top_5_champion_masteries[key]:
                top_5_champion_masteries[key] = champion_dict[value]

    top_5_champion_masteries = dict([(value, key) for key, value in top_5_champion_masteries.items()])
    summoner_stats += "Top 5 Champions By Mastery Points\n"

    for key in top_5_champion_masteries:
        champion = str(key) + " (" + str(top_5_champion_masteries[key]) + ")\n"
        summoner_stats += champion

    return summoner_stats


if __name__ == "__main__":
    # creates a connection to discord
    client = discord.Client()

    # set a status for the bot
    # client.change_presence(activity=discord.Game("living life"))

    # register an event
    @client.event
    # called when the bot is ready to start being used
    async def on_ready():
        print("we have logged in as {0.user}".format(client))

    @client.event
    # triggers each time a command is received from the user
    async def on_message(message):
        if message.author == client.user:
            return

        # user commands
        if message.content.startswith("-help"):
            await message.channel.send("```"
                                       "Commands           Action\n"
                                       "-hello       ->    Johnson Bot will say hello back to you.\n"
                                       "-yer         ->    YERRRR!\n"
                                       "-play        ->    Play a track!\n"
                                       "-pause       ->    Pause a track!\n"
                                       "-resume      ->    Resume a track!\n"
                                       "-stop        ->    Disconnects bot from channel.\n"
                                       "-inspire     ->    Grab an inspirational quote.\n"
                                       "-meme        ->    Catch a random reddit meme!\n"
                                       "-spongegar   ->    MeMiFY yOUr SEnTeNCe!\n"
                                       "                   -spongegar {your sentence}\n"
                                       "-league      ->    See your LoL stats!\n"
                                       "                   -league {your summoner name}\n"
                                       "-capture     ->    Screenshot a website!\n"
                                       "                   -capture {link to question}\n"
                                       "-yelp        ->    Search for businesses on yelp!\n"
                                       "                   -yelp {your item} @{your location}\n"
                                       "```")

        if message.content.startswith("-hello"):
            await message.channel.send("Hello!")

        if message.content.startswith("-yer"):
            await message.channel.send("YERRRR!")

        if message.content.startswith("-inspire"):
            await message.channel.send(get_inspirational_quote())

        if message.content.startswith("-spongegar "):
            text = message.content
            await message.channel.send(spongegar(text[11:]))

        if message.content.startswith("-play "):
            # check if user is in a voice channel
            if message.author.voice:
                song_name = message.content[6:]

                # check if input is url and if not, search for a youtube url of the input
                if not validators.url(song_name):
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        try:
                            get(song_name)
                        except:
                            video = ydl.extract_info(f"ytsearch:{song_name}", download=False)['entries'][0]
                        else:
                            video = ydl.extract_info(song_name, download=False)
                    song_name = video['webpage_url']

                # song_file = os.path.isfile("song.mp3")
                # try:
                #     if song_file:
                #         os.remove("song.mp3")
                # except PermissionError:
                #     await message.channel.send("Wait for current song to finish or skip/stop the song!")
                #     return

                channel = message.author.voice.channel
                await channel.connect()
                voice = discord.utils.get(client.voice_clients, guild=message.guild)

                for file in os.listdir("./"):
                    if file == "song.mp3":
                        os.remove(file)

                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([song_name])

                for file in os.listdir("./"):
                    if file.endswith(".m4a"):
                        os.rename(file, "song.mp3")
                voice.play(discord.FFmpegPCMAudio("song.mp3"))
            else:
                await message.channel.send("You must be in a voice channel to activate this command!")

        if message.content.startswith("-pause"):
            if message.guild.voice_client:
                voice = discord.utils.get(client.voice_clients, guild=message.guild)
                if voice.is_playing():
                    voice.pause()
            else:
                await message.channel.send("You must be in a voice channel to activate this command!")

        if message.content.startswith("-resume"):
            if message.guild.voice_client:
                voice = discord.utils.get(client.voice_clients, guild=message.guild)
                if voice.is_paused():
                    voice.resume()
            else:
                await message.channel.send("You must be in a voice channel to activate this command!")

        if message.content.startswith("-stop"):
            # checks if bot is in a voice channel
            if message.guild.voice_client:
                await message.guild.voice_client.disconnect()
            else:
                await message.channel.send("I'm not in a voice channel right now!")

        if message.content.startswith("-capture "):
            question = message.content[8:]
            screenshot_website(question)
            await message.channel.send(file=discord.File("pic.jpg"))

        if message.content.startswith("-yelp "):
            yelp_input = message.content
            item = ""
            location = ""

            for c in yelp_input[6:]:
                if c == "@":
                    break
                item += c

            for c in yelp_input[len(item) + 7:]:
                location += c

            result = get_yelp_results(item, location)
            await message.channel.send(f"Displaying Top 5 Results...```{str(result)}```")

        if message.content.startswith("-meme"):
            get_reddit_meme()
            await message.channel.send(file=discord.File("meme.png"))

        if message.content.startswith("-league "):
            summoner_name = message.content[8:]
            await message.channel.send(f"```{get_lol_stats(summoner_name)}```")


    # keep_alive()
    client.run("YOUR_API_KEY")
