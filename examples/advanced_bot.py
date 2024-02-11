import os
import asyncio
from discord.ext import commands
from opentelemetry import trace

# Import the custom trace decorator from your library
from opentelemetry_instrumentation_discordpy.decorators import trace as otel_trace

# Initialize your library's automatic instrumentation (if applicable)
# DiscordPyInstrumentor().instrument()

bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


# Using the @trace decorator for simple automatic span wrapping
@bot.command(name="echo", help="Replies with the same message it receives.")
@otel_trace()
async def echo(ctx, *, message: str):
    await ctx.send(message)


# Direct usage of the OpenTelemetry tracer for complex span control
@bot.command(name="edit", help="Edits a message sent by the bot to say something new.")
async def edit(ctx, *, new_message: str):
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("edit_command"):
        msg = await ctx.send("This message will be edited")
        await asyncio.sleep(5)  # Simulate some delay
        with tracer.start_as_current_span("edit_message_operation"):
            await msg.edit(content=new_message)


# Using the @trace decorator for event handling
@bot.event
@otel_trace()
async def on_message(message):
    if message.author == bot.user:
        return
    # Ensure the bot can still process commands
    await bot.process_commands(message)


# Run the bot with your token
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
bot.run(TOKEN)
