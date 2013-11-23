#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sleekxmpp
import logging

logging.basicConfig(level=logging.DEBUG)

class Olark(sleekxmpp.ClientXMPP):

    def __init__(self, username, password, hipchat_client, hipchat_room):
        super(Olark, self).__init__(username, password)
        self.hipchat_client = hipchat_client
        self.hipchat_room = hipchat_room
        # add listeners
        self.add_event_handler("session_start", self.operator_is_here)
        self.add_event_handler("message", self.visitor_send_message)

    def operator_is_here(self, event):
        """
        When the session starts, this function is called
        """
        self.send_presence()
        self.get_roster()

    def visitor_send_message(self, message):
        """
        When a message is received from HipChat, this function is called
        """
        username = self.get_username(message['from'])
        self.hipchat_client.method('rooms/message', 
            method='POST', 
            parameters={
                'room_id': self.hipchat_room, 
                'from': 'Olark', 
                'message': self.get_message(username, message['body']),
                'notify': 1})

    def get_username(self, from_):
        from_ = str(from_)
        return self.client_roster[from_]['name'] or from_

    def get_message(self, username, body):
        link = "<a href='https://chat.olark.com'>chat.olark.com</a>"
        return "{}: {} -> {}".format(username, body, link)