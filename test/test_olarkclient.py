#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from mock import Mock
from olarkclient import Olark

class TestOlarkClient(unittest.TestCase):

    def setUp(self):
        self.username = 'username'
        self.password = 'password'
        self.hipchat_client = Mock()
        self.hipchat_client.method = Mock(return_value={'room': {'name': 'test1', 'room_id': 2}})
        self.hipchat_room = 'room_name'
        self.client = Olark(self.username, self.password, self.hipchat_client, self.hipchat_room)

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
        username = self.client.get_username(message['from'])
        msg = self.client.get_message(username, message['body'])
        self.client.visitor_send_message(message)
        self.hipchat_client.method.assert_called_with(
        	'rooms/message', 
        	method='POST', 
        	parameters={
                'room_id': self.hipchat_room, 
                'from': 'Olark', 
                'message': msg,
                'notify': 1})

if __name__ == '__main__':
    unittest.main()