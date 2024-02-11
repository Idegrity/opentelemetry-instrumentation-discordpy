# OpenTelemetry Instrumentation for Discord.py

This library provides OpenTelemetry instrumentation for bots built with `discord.py`, making it easy to collect traces, metrics, and logs to analyze the performance and reliability of your Discord bots.

## Features

- Automatic instrumentation for common `discord.py` events and activities.
- Decorators for manual instrumentation of bot commands and event handlers.
- Easy integration with OpenTelemetry's ecosystem for observability and monitoring.

## Installation

Install this package with pip:

```
pip install opentelemetry-instrumentation-discordpy
```

## Usage

### Automatic Instrumentation

To automatically instrument your Discord bot, simply initialize the instrumentation at the start of your bot's code:

```
from opentelemetry_instrumentation_discordpy import DiscordPyInstrumentor
DiscordPyInstrumentor().instrument()
```

### Manual Instrumentation

For more fine-grained control, use the provided decorators to instrument specific commands or event handlers:

```
from opentelemetry_instrumentation_discordpy import trace
from opentelemetry_instrumentation_discordpy.decorators import trace as otel_trace

@trace()
async def on_message(message):
    if message.author == bot.user:
        return

    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("on_message_event"):
        print(f"Message from {message.author}: {message.content}") # replace with logic you'd like the bot to trace
        # Ensure the bot can still process commands
        await bot.process_commands(message)

# option 1 for tracing
@bot.command(name='echo', help='Replies with the same message it receives.')
async def echo(ctx, *, message: str):
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("echo_command"):
        await ctx.send(message)

#option 2 for tracing
@bot.command(name='echo', help='Replies with the same message it receives.')
@otel_trace()
async def echo(ctx, *, message: str):
    await ctx.send(message)
```

For a basic practical example of setting up a bot with OpenTelemetry instrumentation, see the [basic bot example](https://github.com/Idegrity/opentelemetry-instrumentation-discordpy/blob/main/examples/basic_bot.py).

For a more advanceced practical example of setting up a bot with OpenTelemetry instrumentation, see the [advanced bot example](https://github.com/Idegrity/opentelemetry-instrumentation-discordpy/blob/main/examples/advanced_bot.py).

## Configuration

Refer to the [documentation](./docs/usage.md) for detailed configuration options and advanced usage.

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](./docs/contributing.md) for how to get started.

## License

This library is licensed under the [BSD License](LICENSE).

## Support

If you encounter any issues or have questions, please file an issue on GitHub.
