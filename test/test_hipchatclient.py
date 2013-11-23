#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from mock import Mock
from hipchatclient import HipChat

class TestHipchatClient(unittest.TestCase):

    def setUp(self):
        self.room_name = 'room_name'
        self.token = 'token'
        self.client = HipChat(self.token, self.room_name)

    def test_init(self):
        self.assertEqual(self.client.token, self.token)
        self.assertEqual(self.client.room_name, self.room_name)

    def test_get_rooms(self):
        """
        Get rooms from Hipchat

        >>> get_rooms()
        [list of rooms]
        """
        self.client.list_rooms = Mock(return_value={'rooms': [{'name': 'test', 'room_id': 1}, {'name': 'test1', 'room_id': 2}]})
        rooms = self.client.get_rooms()
        self.client.list_rooms.assert_called_with()
        self.assertEqual(len(rooms), 2)

    def test_get_room(self):
        """
        Get room info

        >>> get_rooms('room_name')
        {'name': 'room_name', 'room_id': 'room id'}
        """
        self.client.get_rooms = Mock(return_value=[{'name': 'test', 'room_id': 1}, {'name': 'test1', 'room_id': 2}])
        self.client.method = Mock(return_value={'room': {'name': 'test1', 'room_id': 2}})
        room = self.client.get_room('test1')
        self.client.method.assert_called_with('rooms/show', method='GET', parameters={'room_id': 2})
        self.assertEqual(room.get('room_id'), 2)

    def test_get_participants(self):
        """
        Get participants

        >> get_participants()
        [participants list]
        """
        self.client.get_room = Mock(return_value={'name': 'test1', 'room_id': 2, 'participants': ['test']})
        participants = self.client.get_participants()
        self.client.get_room.assert_called_with('room_name')
        self.assertEqual(len(participants), 1)

if __name__ == '__main__':
    unittest.main()