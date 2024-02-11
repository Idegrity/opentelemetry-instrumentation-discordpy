from opentelemetry import trace
from opentelemetry.instrumentation.utils import wrap as otel_wrap, unwrap as otel_unwrap


def wrap_event_listeners():
    """
    Wraps discord.py event listeners (e.g., on_message) for tracing.
    """
    _wrap_on_message()


def _wrap_on_message():
    """
    Wraps the on_message event listener to trace message reception operations.
    """
    from discord.client import Client

    def on_message_wrapper(wrapped, instance, args, kwargs):
        # Assuming the first argument is the message
        message = args[0]
        tracer = trace.get_tracer("discord.py", "1.0.0")

        # Use message content or type as span name, or simply "on_message"
        span_name = "on_message: " + str(message.type)

        with tracer.start_as_current_span(span_name):
            # You can set attributes related to the message here
            return wrapped(*args, **kwargs)

    otel_wrap(Client, "on_message", on_message_wrapper)


def unwrap_event_listeners():
    """
    Removes instrumentation from event listeners.
    """
    _unwrap_on_message()


def _unwrap_on_message():
    """
    Removes wrapping from the on_message event listener.
    """
    from discord.client import Client

    otel_unwrap(Client, "on_message")
