from opentelemetry import trace
from opentelemetry.instrumentation.utils import wrap as otel_wrap, unwrap as otel_unwrap


def wrap_message_operations():
    """
    Wraps discord.py message operations (e.g., send, edit, delete) for tracing.
    """
    _wrap_send_message()
    _unwrap_edit_message()


def _wrap_send_message():
    """
    Wraps the TextChannel.send method to trace message sending operations.
    """
    from discord import TextChannel

    def send_wrapper(wrapped, instance, args, kwargs):
        tracer = trace.get_tracer("discord.py", "1.0.0")
        with tracer.start_as_current_span("TextChannel.send"):
            # You can add custom attributes to the span here
            return wrapped(*args, **kwargs)

    otel_wrap(TextChannel, "send", send_wrapper)


def _wrap_edit_message():
    """
    Wraps the Message.edit method to trace message editing operations.
    """
    from discord import Message

    def edit_wrapper(wrapped, instance, args, kwargs):
        tracer = trace.get_tracer("discord.py", "1.0.0")
        with tracer.start_as_current_span("Message.edit"):
            return wrapped(*args, **kwargs)

    otel_wrap(Message, "edit", edit_wrapper)


def unwrap_message_operations():
    """
    Removes instrumentation from message operations.
    """
    _unwrap_send_message()
    _wrap_edit_message()


def _unwrap_send_message():
    """
    Removes wrapping from the TextChannel.send method.
    """
    from discord import TextChannel

    otel_unwrap(TextChannel, "send")


def _unwrap_edit_message():
    """
    Removes wrapping from the Message.edit method.
    """
    from discord import Message

    otel_unwrap(Message, "edit")
