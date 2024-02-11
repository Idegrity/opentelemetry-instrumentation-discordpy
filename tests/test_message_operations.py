import unittest
from unittest.mock import patch, MagicMock
import asyncio
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import InMemorySpanExporter, SimpleSpanProcessor
from opentelemetry_instrumentation_discordpy.wrappers import message_operations


class TestMessageOperations(unittest.TestCase):
    def setUp(self):
        # Set up the OpenTelemetry test environment
        self.tracer_provider = TracerProvider()
        self.memory_exporter = InMemorySpanExporter()
        self.tracer_provider.add_span_processor(
            SimpleSpanProcessor(self.memory_exporter)
        )
        trace.set_tracer_provider(self.tracer_provider)
        # Setup instrumentation
        message_operations.wrap_message_operations()

    def tearDown(self):
        # Remove instrumentation
        message_operations.unwrap_message_operations()
        # Clean up and reset the test environment
        self.memory_exporter.clear()

    @patch("discord.TextChannel.send")
    def test_send_message_instrumentation(self, mock_send):
        # Mocking discord.py's TextChannel.send to simulate sending a message
        mock_send.return_value = None

        # Simulate sending a message
        # Verify a span was started
        self.assertEqual(len(self.memory_exporter.get_finished_spans()), 1)
        span = self.memory_exporter.get_finished_spans()[0]
        self.assertEqual(span.name, "TextChannel.send")

    @patch("discord.Message.edit")
    async def test_edit_message_instrumentation(self, mock_edit):
        # Mocking discord.Message.edit to simulate editing a message
        mock_edit.return_value = asyncio.Future()
        mock_edit.return_value.set_result(MagicMock())

        # Simulate editing a message
        await mock_edit(content="New content")

        # Verify a span was started for the edit operation
        spans = self.memory_exporter.get_finished_spans()
        self.assertEqual(len(spans), 1)
        span = spans[0]
        self.assertEqual(span.name, "Message.edit")


if __name__ == "__main__":
    unittest.main()
