import unittest

from server import handle_message
from utils import load_configs


class ServerTestCase(unittest.TestCase):
    CONFIGS = load_configs(True)

    test_message = {
        CONFIGS['ACTION']: 'presence',
        CONFIGS['TIME']: 1.1,
        CONFIGS['USER']: {
            CONFIGS['ACCOUNT_NAME']: 'Guest'
        },
        CONFIGS['PRESENCE']: 'presence',
    }
    positive_response = {CONFIGS.get('RESPONSE'): 200}
    negative_response = {
        CONFIGS.get('RESPONSE'): 400,
        CONFIGS.get('ERROR'): 'Bad request'
    }

    def test_correct_response(self):
        test = handle_message(self.test_message, CONFIGS=self.CONFIGS)
        self.assertEqual(test, self.positive_response)

    def test_wrong_action(self):
        self.test_message[self.CONFIGS['ACTION']] = 'wrong'
        test = handle_message(self.test_message, CONFIGS=self.CONFIGS)
        self.assertEqual(test, self.negative_response)

    def test_without_action(self):
        self.test_message.pop(self.CONFIGS['ACTION'])
        test = handle_message(self.test_message, CONFIGS=self.CONFIGS)
        self.assertEqual(test, self.negative_response)

    def test_without_time(self):
        self.test_message.pop(self.CONFIGS['TIME'])
        test = handle_message(self.test_message, CONFIGS=self.CONFIGS)
        self.assertEqual(test, self.negative_response)

    def test_without_user(self):
        self.test_message.pop(self.CONFIGS['USER'])
        test = handle_message(self.test_message, CONFIGS=self.CONFIGS)
        self.assertEqual(test, self.negative_response)

    def test_wrong_user(self):
        self.test_message[self.CONFIGS['USER']] = 'Admin'
        test = handle_message(self.test_message, CONFIGS=self.CONFIGS)
        self.assertEqual(test, self.negative_response)


if __name__ == '__main__':
    unittest.main()
