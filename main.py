import discord
from discord.ext import tasks, commands
import itertools
import os  # <-- needed for secrets

TOKEN = os.environ['DISCORD_TOKEN']  # Bot token from secrets
CHANNEL_ID = 123456789012345678

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

ads = [
    {"title": "🎉 Event 1!", "description": "Join now!", "color": 0xFF0000, "image": "IMAGE_URL_1"},
    {"title": "🔥 Event 2!", "description": "Limited time!", "color": 0x00FF00, "image": "IMAGE_URL_2"}
]

ads_cycle = itertools.cycle(ads)
message = None

@bot.event
async def on_ready():
    global message
    print(f"Logged in as {bot.user}")
    channel = bot.get_channel(CHANNEL_ID)
    ad = next(ads_cycle)
    embed = discord.Embed(title=ad["title"], description=ad["description"], color=ad["color"])
    embed.set_image(url=ad["image"])
    message = await channel.send(embed=embed)
    rotate_ads.start()

@tasks.loop(seconds=30)
async def rotate_ads():
    global message
    ad = next(ads_cycle)
    embed = discord.Embed(title=ad["title"], description=ad["description"], color=ad["color"])
    embed.set_image(url=ad["image"])
    await message.edit(embed=embed)

bot.run(TOKEN)
