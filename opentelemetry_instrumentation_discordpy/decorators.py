from opentelemetry import trace
from functools import wraps


def trace():
    """
    Decorator to trace bot commands and event handlers.
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            tracer = trace.get_tracer("discord.py")

            # You might want to customize the span name based on the function
            # or include additional attributes based on args or kwargs
            with tracer.start_as_current_span(func.__name__):
                return await func(*args, **kwargs)

        return wrapper

    return decorator
