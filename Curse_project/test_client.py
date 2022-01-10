import unittest

from client import create_presence_message, handle_response
from utils import load_configs


class ClientTestCase(unittest.TestCase):
    CONFIGS = load_configs()

    def test_create_presence_message(self):
        test = create_presence_message('Guest', CONFIGS=self.CONFIGS)
        test[self.CONFIGS['TIME']] = 1.1

        self.assertEqual(
            test,
            {
                self.CONFIGS.get('ACTION'): self.CONFIGS.get('PRESENCE'),
                self.CONFIGS['TIME']: 1.1,
                self.CONFIGS.get('USER'): {
                    self.CONFIGS.get('ACCOUNT_NAME'): 'Guest'
                        }
            })

    def test_handle_response(self):
        # correct request
        test_message = {self.CONFIGS['RESPONSE']: 200}
        test = handle_response(test_message, CONFIGS=self.CONFIGS)
        self.assertEqual(test, '200 : OK')
        # wrong request
        test_message = {self.CONFIGS['RESPONSE']: 400, self.CONFIGS['ERROR']: 'Bad request'}
        test = handle_response(test_message, CONFIGS=self.CONFIGS)
        self.assertEqual(test, '400 : Bad request')
        # ValueError
        test_message.pop(self.CONFIGS['RESPONSE'])
        self.assertRaises(ValueError, handle_response, test_message, self.CONFIGS)


if __name__ == '__main__':
    unittest.main()
