import discord
import requests
from discord.ext import commands



# All API calls are heavily rate-limited; please refer to the Olympus API Documentation for up-to-date information.
# The author is not responsible for any administrative actions due to misuse or other factors.
# Misuse of the API will be the sole responsibility of the user.
# It is imperative to comply with the usage guidelines and rate limits as specified in the Olympus API documentation to ensure responsible and fair use of the service.


# Define intents
intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent

# Initialize the bot with intents
bot = commands.Bot(command_prefix='/', intents=intents)

# LEGACY SUPPORT, Replace these with your actual token and API token, DO NOT USE, only use when testing
# DISCORD_TOKEN = ''
# API_TOKEN = ''

# Discord Token Location
with open('Project_Location/Discord_Token.txt','r') as file:
    DISCORD_TOKEN = file.read().strip()

# Oly API Token Location
with open('Projection_Location/Oly_Token.txt','r') as file:
    API_TOKEN = file.read().strip()

def format_player_data(player_data):
    if not player_data:
        return "No data found for this player."

    # Summarize the data
    player = player_data[0]  # Assuming the first element is the relevant player
    summary = (
        f"Name: {player['name']}\n"
        f"Bank: ${player['bank']}\n"
        f"Cash: ${player['cash']}\n"
        f"Gang: {player.get('gang', {}).get('gang_name', 'No gang')}\n"
        f"Last Active: {player['last_active']}\n"
        f"Total Kills: {player['kills']}\n"
        f"Total Deaths: {player['deaths']}\n"
        # Add more fields as necessary
    )
    return summary

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def players(ctx, player_id):
    url = f'https://stats.olympus-entertainment.com/api/v3.0/players/?player_ids={player_id}'
    headers = {
        'accept': 'application/json',
        'Authorization': f'Token {API_TOKEN}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        player_data = response.json()
        summary_message = format_player_data(player_data)
        await ctx.send(summary_message)
    else:
        await ctx.send('Error fetching player data')

@bot.command()
async def servers(ctx):
    url = 'https://stats.olympus-entertainment.com/api/v3.0/servers/'
    headers = {
        'accept': 'application/json',
        'Authorization': f'Token {API_TOKEN}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        await ctx.send(response.json())
    else:
        await ctx.send('Error fetching server status')

@bot.command()
async def gang(ctx, gang_id):
    url = f'https://stats.olympus-entertainment.com/api/v3.0/gangs/{gang_id}'
    headers = {
        'accept': 'application/json',
        'Authorization': f'Token {API_TOKEN}'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        await ctx.send(response.json())
    else:
        await ctx.send('Error fetching gang data')

bot.run(DISCORD_TOKEN)