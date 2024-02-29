import discord
from discord.commands import Option
from dotenv import load_dotenv
import os
import yaml

def run_bot():
    with open("config.yml", "r") as config_file:
        config = yaml.safe_load(config_file)
    
    
    TOKEN: str = config["TOKEN"]

    intents = discord.Intents.default()

    bot = discord.Bot(
        intents=intents,
        debug_guilds=config["DEBUG_GUILDS"]
    
    )
    @bot.event
    async def on_ready():
        print(f'{bot.user} logged in')

    bot.load_extension("cogs.notification")

    bot.run(TOKEN)

if __name__ == '__main__':
     run_bot()