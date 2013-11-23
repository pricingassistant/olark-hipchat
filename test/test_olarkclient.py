#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import unittest

from mock import Mock
from olarkclient import Olark

logging.basicConfig(level=logging.ERROR)


class TestOlarkClient(unittest.TestCase):

    def setUp(self):
        self.username = 'username'
        self.password = 'password'
        self.queue = Mock()
        self.hipchat_room = 'room_name'
        self.client = Olark(self.queue, self.username, self.password, self.hipchat_room)


    def test_init(self):
        #self.assertEqual(self.client.username, self.username)
        #self.assertEqual(self.client.password, self.password)
        self.assertEqual(self.client.hipchat_room, self.hipchat_room)


    def test_operator_is_here(self):
        """
        
        """
        self.client.send_presence = Mock()
        self.client.get_roster = Mock()
        event = Mock()
        self.client.operator_is_here(event)
        self.client.send_presence.assert_called_with()
        self.client.get_roster.assert_called_with()


    def test_visitor_send_message(self):
        """

        """
        message = {'body': 'body', 'from': 'webuser4.test@test.fr'}
        username = message['from']
        self.client.get_username = Mock(return_value=username)
        self.client.visitor_send_message(message)
        self.queue.put.assert_called_with((username, message['body']))

if __name__ == '__main__':
    unittest.main()