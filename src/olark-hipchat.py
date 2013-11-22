#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hipchat
import config
from olarkclient import Olark

def send_message_to_operator(olark, hipster, msg):
    hipster.method('rooms/message', method='POST', parameters={'room_id': 'test', 'from': msg['from'], 'message': msg['body']})

def session_start(olark):
    olark.send_presence()
    olark.get_roster()

if __name__ == '__main__':
    print 'test'

    hipchat_client = hipchat.HipChat(token=config.HIPCHAT_TOKEN)

    for room in hipchat_client.list_rooms()['rooms']:
        if room.get('name') == config.HIPCHAT_ROOMNAME:
            room_info = hipchat_client.method('rooms/show', method='GET', parameters={'room_id': room.get('room_id')})
            participants = room_info.get('room').get('participants')
            break

    if participants:
        print 'connect to olark'
        olark = Olark(config.OLARK_USERNAME, config.OLARK_PASSWORD, hipchat_client, config.HIPCHAT_ROOMNAME)
        if olark.connect(("olark.com", 5222)):
            olark.process()
            print("Done")
        else:
            print("Unable to connect.")

        while True:
            command = raw_input()
            if command == "e":
                olark.disconnect()
                print "exit"