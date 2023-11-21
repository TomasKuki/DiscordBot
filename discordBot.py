import discord
import requests
import json
from datetime import datetime
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

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
    if RIOT_API_KEY != 'RIOT_API_KEY' :
        
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
    else:
        await ctx.send("Contact the developer for the Riot related services")

@bot.command()
async def player_mastery(ctx, player_name):
    if RIOT_API_KEY != 'RIOT_API_KEY' :
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
    else:
        await ctx.send("Contact the developer for the Riot related services")


@bot.command()
async def learn_this(ctx):
    # Verifica se o comando foi chamado em um servidor (guild)
    if ctx.guild is not None:
        # Verifica se o autor da mensagem anexou um arquivo
        if ctx.message.attachments:
            # Pega o primeiro arquivo anexado
            attachment = ctx.message.attachments[0]

            # Verifica se o arquivo é um CSV
            if attachment.filename.endswith('.csv'):
                # Cria uma pasta chamada "csv_files" se não existir
                if not os.path.exists('csv_files'):
                    os.makedirs('csv_files')

                # Baixa o arquivo para a pasta
                file_path = os.path.join('csv_files', attachment.filename)
                await attachment.save(file_path)
                await ctx.send(f'Arquivo CSV recebido!')

                """# Read CSV file into a pandas DataFrame
                data = pd.read_csv(file_path)

                # Assuming the last column is the target variable and the rest are features
                X = data.iloc[:, :-1]
                y = data.iloc[:, -1]

                # Split the data into training and testing sets
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

                # Initialize a Random Forest classifier (you can choose a different model based on your needs)
                model = RandomForestClassifier()

                # Train the model
                model.fit(X_train, y_train)

                # Make predictions on the test set
                y_pred = model.predict(X_test)

                # Evaluate the accuracy of the model
                accuracy = accuracy_score(y_test, y_pred)
                print(f"Model accuracy: {accuracy:.2f}")

                # Save the trained model to a file
                model_filename = "trained_model.joblib"
                joblib.dump(model, model_filename)
                print(f"Trained model saved to {model_filename}")

                await ctx.send(f'Ai Name Trained')"""
            else:
                await ctx.send('Por favor, anexe um arquivo CSV.')
        else:
            await ctx.send('Por favor, anexe um arquivo CSV.')
    else:
        await ctx.send('Este comando só pode ser usado em um servidor (guild).')

bot.run('MzI3NTEzMzgyNDM5NjE2NTEy.GYLW-H.nOQbJXAoc73w69qgfVJJouMpR1JNpyR6zAGhIc')
