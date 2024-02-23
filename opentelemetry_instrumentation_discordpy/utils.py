from opentelemetry.trace import Span, get_current_span
from discord import Message


def extract_message_attributes(message: Message) -> dict:
    """
    Extracts attributes from a discord.py Message object to be set as span attributes.

    Parameters:
    - message: The Message object from which to extract information.

    Returns:
    A dictionary of span attributes.
    """
    attributes = {
        "discord.channel_id": str(message.channel.id),
        "discord.guild_id": str(message.guild.id) if message.guild else None,
        "discord.message_id": str(message.id),
        "discord.author_id": str(message.author.id),
        "discord.content": message.content,
    }
    # Be mindful of PII and sensitive information before adding content or similar attributes.
    return attributes


def add_span_attributes_from_message(span: Span, message: Message):
    """
    Adds extracted Message attributes to the current span.

    Parameters:
    - span: The Span to which attributes should be added.
    - message: The Message object from which to extract information.
    """
    attributes = extract_message_attributes(message)
    for key, value in attributes.items():
        if value is not None:
            span.set_attribute(key, value)


def wrap(target, attribute, wrapper):
    """
    Replace a function or method on the target object with a wrapper function.

    Parameters:
    - target: The object that contains the function/method.
    - attribute: The name of the function/method as a string.
    - wrapper: A function that returns the wrapped function/method.
    """
    original = getattr(target, attribute)
    wrapped = wrapper(original)
    setattr(target, attribute, wrapped)
    setattr(wrapped, "__original__", original)


def unwrap(target, attribute):
    """
    Restore the original function or method on the target object.

    Parameters:
    - target: The object that contains the function/method.
    - attribute: The name of the function/method as a string.
    """
    wrapped = getattr(target, attribute)
    original = getattr(wrapped, "__original__", None)
    if original:
        setattr(target, attribute, original)
