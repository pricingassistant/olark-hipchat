#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sleekxmpp


class Olark(sleekxmpp.ClientXMPP):

    def __init__(self, queue, username, password, hipchat_room):
        super(Olark, self).__init__(username, password)
        self.queue = queue
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
        # get the username
        username = self.get_username(message['from'])
        # add this message to the queue
        self.queue.put((username, message['body']))


    def get_username(self, from_):
        from_ = str(from_)
        return self.client_roster[from_]['name'] or from_