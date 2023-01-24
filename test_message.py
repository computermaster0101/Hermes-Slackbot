import unittest
import json
import datetime
from message import Message


class TestMessage(unittest.TestCase):
    def setUp(self):
        self.valid_message_file = 'valid_message.json'
        self.valid_message_object = {
            "device": "device1",
            "message": "Hello",
            "timestamp": "2022-01-01T00:00:00"
        }
        self.invalid_message_file = 'invalid_message.json'
        self.invalid_message_object = {
            "device": "device1",
            "message": "Hello"
        }
        self.nonexistent_message_file = 'nonexistent_message.json'
        
    def test_valid_message_file(self):
        with open(self.valid_message_file, 'w') as f:
            json.dump(self.valid_message_object, f)
        
        message = Message(message_file=self.valid_message_file)
        self.assertEqual(message.device, "device1")
        self.assertEqual(message.text, "Hello")
        self.assertEqual(message.timestamp, "2022-01-01T00:00:00")
        
    def test_valid_message_object(self):
        message = Message(message_object=self.valid_message_object)
        self.assertEqual(message.device, "device1")
        self.assertEqual(message.text, "Hello")
        self.assertEqual(message.timestamp, "2022-01-01T00:00:00")
        
    def test_invalid_message_file(self):
        with open(self.invalid_message_file, 'w') as f:
            json.dump(self.invalid_message_object, f)
        
        with self.assertRaises(ValueError) as context:
            message = Message(message_file=self.invalid_message_file)
        self.assertEqual(str(context.exception), "Error: Missing attributes in message file")
        
    def test_invalid_message_object(self):
        with self.assertRaises(ValueError) as context:
            message = Message(message_object=self.invalid_message_object)
        self.assertEqual(str(context.exception), "Error: Missing attributes in message object")
        
    def test_nonexistent_message_file(self):
        with self.assertRaises(FileNotFoundError) as context:
            message = Message(message_file=self.nonexistent_message_file)
        self.assertEqual(str(context.exception), f"Error: {self.nonexistent_message_file} does not exist.")
        
    def tearDown(self):
        # Delete all test files
        for file in [self.valid_message_file,self.invalid_message_file]:
            try:
                os.remove(file)
            except:
                pass

if __name__ == '__main__':
    unittest.main()