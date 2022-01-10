import unittest
import mock
import json

from utils import send_message, get_message, load_configs


class TestSocket:
    CONFIGS = load_configs()

    def __init__(self, test_message):
        self.test_message = test_message
        self.encoded_message = None
        self.received_message = None

    def send(self, message_to_send):
        json_test_message = json.dumps(self.test_message)
        self.encoded_message = json_test_message.encode(self.CONFIGS['ENCODING'])
        self.received_message = message_to_send

    def recv(self, max_len):
        json_test_message = json.dumps(self.test_message)
        return json_test_message.encode(self.CONFIGS['ENCODING'])


class Tests(unittest.TestCase):
    CONFIGS = load_configs(True)

    test_message_send = {
        CONFIGS['ACTION']: CONFIGS['PRESENCE'],
        CONFIGS['TIME']: 1111.1111,
        CONFIGS['USER']: {
            CONFIGS['ACCOUNT_NAME']: 'test_test'
        }
    }

    test_success_receive = {CONFIGS['RESPONSE']: 200}
    test_error_receive = {
        CONFIGS['RESPONSE']: 400,
        CONFIGS['ERROR']: 'Bad request'
    }

    def test_send_message(self):
        test_socket = TestSocket(self.test_message_send)
        send_message(test_socket, self.test_message_send, self.CONFIGS)
        self.assertEqual(test_socket.encoded_message, test_socket.received_message)
        with self.assertRaises(Exception):
            send_message(test_socket, test_socket, self.CONFIGS)

    def test_get_message(self):
        test_sock_ok = TestSocket(self.test_success_receive)
        test_sock_err = TestSocket(self.test_error_receive)
        self.assertEqual(get_message(test_sock_ok, self.CONFIGS), self.test_success_receive)
        self.assertEqual(get_message(test_sock_err, self.CONFIGS), self.test_error_receive)


if __name__ == '__main__':
    unittest.main()


# test_socket = "<socket.socket fd=244, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, " \
#               "proto=0, laddr=('127.0.0.1', 58299), raddr=('127.0.0.1', 7777)>"
# test_message = {CONFIGS['RESPONSE']: 200}
# mock_socket = mock.Mock()
# mock_socket.bind(('127.0.0.1', 7777))
# print(mock_socket.recv.return_value)
# print(send_message(mock_socket, test_message, CONFIGS))
# with mock.patch('socket.socket') as mock_socket:
#     mock_socket.return_value.recv.return_value = test_socket
# print(send_message(mock_socket, test_message, CONFIGS))
# print(mock_socket)
