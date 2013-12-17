#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hipchat
import logging
import Queue
import signal
import time
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__)))

import config
from olarkclient import Olark
from hipchatclient import HipChat
from threading import Thread


logging.basicConfig(level=logging.ERROR)


class OlarkHipchat(Thread):

    def __init__(self, sleep_delay, hipchat_client, olark_client):
        super(OlarkHipchat, self).__init__()
        self.sleep_delay = sleep_delay
        self.running = True
        self.hipchat_client = hipchat_client
        self.olark_client = olark_client

    def run(self):
        while self.running:
            # monitor if there is a participant in the HipChat room
            participants = self.hipchat_client.get_participants()

            # get the olark client state
            olark_state = self.olark_client.state.current_state()

            # print "pp", participants, olark_state

            # if participants and olark client is not connected
            if participants and olark_state != "connected":
                # connect it
                if self.olark_client.connect(("olark.com", 5222)):
                    self.olark_client.process()

            # if no participant, disconnect olark client
            elif not participants and olark_state == "connected":
                self.olark_client.disconnect()

            # wait to check again Hipchat participants
            time.sleep(self.sleep_delay)

    def stop(self):
        self.running = False

if __name__ == '__main__':
    # create the queue
    queue = Queue.Queue(maxsize=0)

    # create clients for Olark and HipChat
    hipchat_client = HipChat(queue, config.HIPCHAT_TOKEN, config.HIPCHAT_ROOMNAME)
    hipchat_client.start()
    olark_client = Olark(queue, config.OLARK_USERNAME, config.OLARK_PASSWORD, config.HIPCHAT_ROOMNAME)

    # create the watch dog
    client = OlarkHipchat(config.HIPCHAT_SLEEPDELAY, hipchat_client, olark_client)
    client.start()

    # CTRL + C -> quit the application
    def handler(signum, frame):
        client.stop()
	try:
        	olark_client.abort()
	except:
		pass
	try:
		hipchat_client.stop()
	except:
		pass
    signal.signal(signal.SIGINT, handler)
    signal.pause()
