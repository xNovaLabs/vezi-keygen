import discord
import secrets
from discord.ext import commands
import json
import os
from dotenv import load_dotenv
load_dotenv()
import json

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='/', intents=intents)


@bot.hybrid_command()
async def sync(ctx: commands.Context):
    await ctx.send(f'Syncing commands for {len(bot.guilds)} guilds.')
    await bot.tree.sync()


@bot.hybrid_command()
async def getkey(ctx: commands.Context):
    with open("keys.json", "r") as f:
        data = json.load(f)

    hello = False
    for key in data:
        if key == str(ctx.message.author.id):
            await ctx.send("You already have an API Key!")
            hello = True
    
    if not hello:
        keys = "vezi-" + str(secrets.token_urlsafe(16))

        data[str(ctx.message.author.id)] = {"key": keys, "usage": 350}

        with open("keys.json", "w") as f:
            json.dump(data, f, indent=4)

        await ctx.message.author.send(keys)
        await ctx.send("Key sent to your dms.")

@bot.hybrid_command()
async def usage(ctx: commands.Context):
    with open("keys.json", "r") as f:
        data = json.load(f)

    hello = False
    for key in data:
        if key == str(ctx.message.author.id):
            await ctx.send("Daily Usage Left: " + str(key["usage"]))
            hello = True
    if not hello:
        await ctx.send("No API Key Present.")
    
    

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.tree.sync()



bot.run(os.getenv('DISCORD_TOKEN'))