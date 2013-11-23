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
        msg = "{} -> <a href='https://chat.olark.com'>chat.olark.com</a>".format(message['body'])
        username = str(message['from']).split(".")[0]
        self.hipchat_client.method('rooms/message', 
            method='POST', 
            parameters={
                'room_id': self.hipchat_room, 
                'from': username, 
                'message': msg,
                'notify': 1})