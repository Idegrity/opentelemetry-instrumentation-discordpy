from opentelemetry import trace
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from .utils import wrap as otel_wrap, unwrap as otel_unwrap


class DiscordPyInstrumentor(BaseInstrumentor):
    """An instrumentor for discord.py

    This instrumentor automatically traces key discord.py operations, such as command processing and message sending.
    """

    _instrumented = False

    def _instrument(self, **kwargs):
        """Instrument discord.py operations"""
        if self._instrumented:
            return

        # Instrument command processing
        from discord.ext.commands import Bot

        otel_wrap(
            "discord.ext.commands",
            "Bot.process_commands",
            self._wrapper_process_commands,
        )

        # Instrument message sending
        from discord.channel import TextChannel

        otel_wrap("discord.channel", "TextChannel.send", self._wrapper_send_message)

        self._instrumented = True

    def _uninstrument(self, **kwargs):
        """Uninstrument discord.py operations"""
        if not self._instrumented:
            return

        # Uninstrument command processing
        otel_unwrap("discord.ext.commands", "Bot.process_commands")

        # Uninstrument message sending
        otel_unwrap("discord.channel", "TextChannel.send")

        self._instrumented = False

    def _wrapper_process_commands(self, original, instance, args, kwargs):
        """Wrapper for the Bot.process_commands method"""
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("Bot.process_commands"):
            # Call the original process_commands method
            return original(*args, **kwargs)

    def _wrapper_send_message(self, original, instance, args, kwargs):
        """Wrapper for the TextChannel.send method"""
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("TextChannel.send"):
            # Call the original send method
            return original(*args, **kwargs)
