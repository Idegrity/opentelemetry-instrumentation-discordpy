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
