#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sleekxmpp

class Olark(sleekxmpp.ClientXMPP):

	def __init__(self, username, password, hipchat_client, hipchat_room):
		sleekxmpp.ClientXMPP.__init__(self, username, password)
		self.hipchat_client = hipchat_client
		self.hipchat_room = hipchat_room
		self.add_event_handler("session_start", self.operator_is_here)
		self.add_event_handler("message", self.visitor_send_message)

	def operator_is_here(self, event):
		"""

		"""
		#self.send_presence()
        #self.get_roster()

	def visitor_send_message(self, message):
		hipchat_client.method('rooms/message', method='POST', parameters={'room_id': self.hipchat_room, 'from': message['from'], 'message': message['body']})