#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hipchat
import config
from olarkclient import Olark
from hipchatclient import HipChat
from threading import Thread
import time
import signal, os

class OlarkHipchat(Thread):

    def __init__(self, sleep_delay):
        super(OlarkHipchat, self).__init__()
        self.sleep_delay = sleep_delay
        self.running = True

    def run(self):
        # create clients for Olark and HipChat
        self.hipchat_client = HipChat(config.HIPCHAT_TOKEN, config.HIPCHAT_ROOMNAME)
        self.olark_client = Olark(config.OLARK_USERNAME, config.OLARK_PASSWORD, self.hipchat_client, config.HIPCHAT_ROOMNAME)

        while self.running:
            # monitor if there is a participant in the HipChat room
            participants = self.hipchat_client.get_participants()
            # get the olark client state
            olark_state = self.olark_client.state.current_state()

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
        self.olark_client.abort()



if __name__ == '__main__':
    client = OlarkHipchat(config.HIPCHAT_SLEEPDELAY)
    client.start()

    def handler(signum, frame):
        print 'Signal handler called with signal', signum
        client.stop()

    signal.signal(signal.SIGINT, handler)
    signal.pause()
