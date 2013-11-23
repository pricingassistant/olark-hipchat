#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hipchat

from threading import Thread


class HipChat(hipchat.HipChat):

    def __init__(self, queue, token, room_name):
        super(HipChat, self).__init__(token=token)
        self.queue = queue
        self.room_name = room_name
        self.room = None
        self.running = True
    

    def get_participants(self):
        # get room information
        room = self.get_extended_room_information(self.room_name)
        return room.get('participants')


    def get_extended_room_information(self, name):
        room = self.get_room_information(name)
        # return extended room information
        return self.method('rooms/show', 
            method='GET', 
            parameters={'room_id': room.get('room_id')}).get('room')


    def get_room_information(self, name):
        # if no room information, get it
        if self.room is None or (self.room.get('name') != name):
            for room in self.get_rooms():
                if room.get('name') == name:
                    self.room = room
        return self.room


    def get_rooms(self):
        # get rooms from hipchat
        return self.list_rooms()['rooms']


    def send_message(self, username, message):
        # send message to hipchat
        self.method('rooms/message', 
            method='POST', 
            parameters={
                'room_id': self.room.get('room_id'), 
                'from': 'Olark', 
                'message': self.get_formatted_message(username, message),
                'notify': 1})


    def get_formatted_message(self, username, message):
        link = "<a href='https://chat.olark.com'>chat.olark.com</a>"
        return "{}: {} -> {}".format(username, message, link)


    def worker(self):
        # listen the queue to send messages from Olark to Hipchat
        while self.running:
            (username, message) = self.queue.get()
            if username and message:
                self.send_message(username, message)


    def start(self):
        # start the queue listening
        t = Thread(target=self.worker)
        t.start()


    def stop(self):
        self.running = False
        self.queue.put((None, None))
