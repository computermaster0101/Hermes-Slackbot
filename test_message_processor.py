import unittest

import unittest
import os
import json
from message_processor import MessageProcessor
from message import Message
from rule import Rule


class TestMessageProcessor(unittest.TestCase):

    def setUp(self):
        self.message = Message(message_object={'device': 'device1', 'message': 'test message', 'timestamp': '2022-01-01 12:00:00'})
        self.rules = [Rule(file) for file in os.listdir('test_rules') if file.endswith('.json')]
        self.message_processor = MessageProcessor(rules=self.rules)

    def test_process_message(self):
        result = self.message_processor.process_message(self.message)
        self.assertIsInstance(result, bool)

    def test_run_actions(self):
        self.message_processor.run_actions(self.message, self.rules[0].actions)
        self.assertTrue(os.path.exists('test_output'))

    def test_match_pattern(self):
        result = self.message_processor.match_pattern(self.message.text, self.rules[0].patterns)
        self.assertIsInstance(result, bool)


if __name__ == '__main__':
    unittest.main()
