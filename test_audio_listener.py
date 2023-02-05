import unittest
from audio_listener import audio_listener


class TestAudioListener(unittest.TestCase):

    def setUp(self):
        self.al = audio_listener()
        self.al.keyword = "computer"
        self.al.system_name = "computer"

    # def test_listen_for_keyword(self):
    #     self.al.listen_for_keyword()
    #     self.assertTrue(self.al.message)

    def test_remove_keyword(self):
        self.al.remove_keyword("computer hello")
        self.assertEqual(self.al.message['message'], "hello")

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
