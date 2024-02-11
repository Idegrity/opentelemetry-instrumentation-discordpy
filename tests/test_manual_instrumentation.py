import unittest
from unittest.mock import MagicMock
import asyncio
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import InMemorySpanExporter, SimpleSpanProcessor
from opentelemetry_instrumentation_discordpy.decorators import trace


class TestManualInstrumentation(unittest.TestCase):
    def setUp(self):
        # Set up the OpenTelemetry test environment
        self.tracer_provider = TracerProvider()
        self.memory_exporter = InMemorySpanExporter()
        self.tracer_provider.add_span_processor(
            SimpleSpanProcessor(self.memory_exporter)
        )
        trace.set_tracer_provider(self.tracer_provider)

    def tearDown(self):
        # Clean up and reset the test environment
        self.memory_exporter.clear()

    def test_trace_decorator(self):
        @trace()
        async def mock_command(ctx):
            return "mock response"

        # Simulate calling the decorated command
        ctx = MagicMock()
        result = asyncio.run(mock_command(ctx))

        # Verify that a span was started for the mock command
        self.assertEqual(len(self.memory_exporter.get_finished_spans()), 1)
        span = self.memory_exporter.get_finished_spans()[0]
        self.assertEqual(span.name, "mock_command")


if __name__ == "__main__":
    unittest.main()
