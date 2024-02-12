# OpenTelemetry Instrumentation for Discord.py

This library provides OpenTelemetry instrumentation for bots built with `discord.py`, making it easy to collect traces, metrics, and logs to analyze the performance and reliability of your Discord bots.

## Features

- Automatic instrumentation for common `discord.py` events and activities.
- Decorators for manual instrumentation of bot commands and event handlers.
- Easy integration with OpenTelemetry's ecosystem for observability and monitoring.


## Features Overview

The OpenTelemetry Instrumentation for Discord.py is designed to enhance the observability of your Discord bots, providing detailed insights into their operations and interactions. Here are the key features currently implemented:

- **Automatic Tracing**: Automatically instruments your bot to trace key Discord events and activities, ensuring comprehensive visibility with minimal setup.

- **Manual Tracing Support**: Offers decorators and utilities for manual instrumentation, allowing you to tailor tracing to your bot's specific needs and workflows.

- **`send_message` Instrumentation**: Traces calls to `send_message`, providing insights into message sending operations, including execution times and potential bottlenecks.

- **`edit_message` Instrumentation**: Captures detailed information about `edit_message` operations, enabling you to track how message edits affect bot performance and user interactions.

- **`on_message` Event Tracing**: Automatically traces the `on_message` event, offering visibility into message processing and the bot's responsiveness to user messages.

These features are designed to give developers and operators comprehensive insights into the behavior and performance of their Discord bots, facilitating better monitoring, troubleshooting, and optimization.

Do note, this build is currently in alpha so the above featureset is quite small. I will do more to edit it as I get time. 

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

Refer to the [documentation](./docs/usage.md) for detailed configuration options and advanced usage. (This is WIP)

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](https://github.com/Idegrity/opentelemetry-instrumentation-discordpy/blob/main/docs/CONTRIBUTING.md) for how to get started.

## License

This library is licensed under the [BSD License](https://github.com/Idegrity/opentelemetry-instrumentation-discordpy/blob/main/LICENSE).

## Support

If you encounter any issues or have questions, please file an issue on GitHub.
