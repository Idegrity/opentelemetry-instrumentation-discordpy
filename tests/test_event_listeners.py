import unittest
from unittest.mock import patch, MagicMock
from opentelemetry import trace
from opentelemetry_instrumentation_discordpy.wrappers import event_listeners


import unittest
from unittest.mock import patch, MagicMock
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import InMemorySpanExporter, SimpleSpanProcessor
from opentelemetry_instrumentation_discordpy.wrappers import event_listeners


class TestEventListeners(unittest.TestCase):
    def setUp(self):
        self.tracer_provider = TracerProvider()
        self.memory_exporter = InMemorySpanExporter()
        self.tracer_provider.add_span_processor(
            SimpleSpanProcessor(self.memory_exporter)
        )
        trace.set_tracer_provider(self.tracer_provider)
        event_listeners.wrap_event_listeners()

    def tearDown(self):
        event_listeners.unwrap_event_listeners()

    @patch("discord.Client.event")
    def test_on_message_instrumentation(self, mock_event):
        mock_event.return_value = MagicMock()

        # Your test implementation here

        spans = self.memory_exporter.get_finished_spans()
        self.assertEqual(len(spans), 1)
        span = spans[0]
        self.assertTrue(span.name.startswith("on_message"))


if __name__ == "__main__":
    unittest.main()
