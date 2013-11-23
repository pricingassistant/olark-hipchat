#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hipchat

class HipChat(hipchat.HipChat):

	def __init__(self, token, room_name):
		super(HipChat, self).__init__(token=token)
		self.room_name = room_name
		self.room = None

	def get_participants(self):
		# get room information
		room = self.get_room(self.room_name)
		return room.get('participants')

	def get_room(self, name):
		# if no room information, get it
		if self.room is None or (self.room.get('name') != name):
			for room in self.get_rooms():
				if room.get('name') == name:
					self.room = room
		# return room extended information
		return self.method('rooms/show', 
			method='GET', 
			parameters={'room_id': self.room.get('room_id')}).get('room')

	def get_rooms(self):
		# get rooms from hipchat
		return self.list_rooms()['rooms']