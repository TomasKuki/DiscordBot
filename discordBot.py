import discord
import requests
import json
from datetime import datetime

from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

RIOT_API_KEY = 'RIOT_API_KEY'

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

@bot.command()
async def howdy(ctx):
    await ctx.send('Howdy!')

@bot.command()
async def hi(ctx):
    await ctx.send('Hi!')

@bot.command()
async def time(ctx, location):
    url = f'http://worldtimeapi.org/api/timezone/{location}'
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        time = datetime.strptime(data['datetime'], '%Y-%m-%dT%H:%M:%S.%f%z')
        await ctx.send(f'The time in {location} is {time.strftime("%H:%M:%S %p")}')
    else:
        await ctx.send(f'Unable to find time for {location}')

@bot.command()
async def weather(ctx, location):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid=YOUR_API_KEY'
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        temp = data['main']['temp']
        await ctx.send(f'The temperature in {location} is {temp} Kelvin')
    else:
        await ctx.send(f'Unable to find weather for {location}')


@bot.command()
async def translate(ctx, text, from_lang, to_lang):
    params = {
        'q': text,
        'langpair': f'{from_lang}|{to_lang}'
    }

    response = requests.get('https://api.mymemory.translated.net/get', params=params)
    response_json = response.json()
    translated_text = response_json['responseData']['translatedText']
    await ctx.send(translated_text)


@bot.command()
async def player(ctx, player_name):
    url = f'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{player_name}?api_key={RIOT_API_KEY}'
    response = requests.get(url)
    if response.status_code != 200:
        await ctx.send(f'Unable to find player {player_name}')
        return
    player_data = response.json()
    level = player_data['summonerLevel']
    response = requests.get(f'https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{player_data["id"]}?api_key={RIOT_API_KEY}')
    if response.status_code != 200:
        await ctx.send("An error occured, check the player name and region")
        return
    rank_data = response.json()
    rank = rank_data[0]['rank'] if rank_data else "Unranked"
    await ctx.send(f'Level: {level}\nRank: {rank}')

@bot.command()
async def player_mastery(ctx, player_name):
    response = requests.get(f'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{player_name}?api_key={RIOT_API_KEY}')
    if response.status_code != 200:
        await ctx.send("An error occured, check the player name and region")
        return
    player_data = response.json()
    player_id = player_data["id"]
    response = requests.get(f'https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{player_id}?api_key={RIOT_API_KEY}')
    if response.status_code != 200:
        await ctx.send("An error occured, check the player name and region")
        return
    mastery_data = response.json()
    mastery_data = sorted(mastery_data, key=lambda x: x["championPoints"], reverse=True)
    mastery_str = ''
    i=0
    for mastery in mastery_data:
        # load json data from file
        with open('LolChampions.json', 'r') as file:
            data = json.load(file)

            try:
                str(mastery["championId"]) == data[str(mastery["championId"])]
                champName = data[str(mastery["championId"])]['name']
                mastery_str += f'{champName} - Mastery: {mastery["championLevel"]} - Mastery Points: {mastery["championPoints"]}\n'
            except KeyError:
                champName = 'Name unavailable'
        i += 1
        if i == 10:
            break
    await ctx.send(f'{player_name} Mastery Champions: \n{mastery_str} \n Please note that support for all champions is not yet available!')


bot.run('Your_Bot_Token')
