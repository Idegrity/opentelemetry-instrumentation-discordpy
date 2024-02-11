import os
from discord.ext import commands
from opentelemetry_instrumentation_discordpy import DiscordPyInstrumentor

# Initialize OpenTelemetry automatic instrumentation
DiscordPyInstrumentor().instrument()

# Create a bot instance
bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    print(f"Message from {message.author}: {message.content}")
    await message.channel.send("Message received!")


# Run the bot with your token
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
bot.run(TOKEN)
