#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hipchat
import config
from olarkclient import Olark
from hipchatclient import HipChat
from threading import Thread
import time

class OlarkHipchat(Thread):

    def __init__(self, sleep_delay):
        super(OlarkHipchat, self).__init__()
        self.sleep_delay = sleep_delay

    def run(self):
        # create clients for Olark and HipChat
        hipchat_client = HipChat(config.HIPCHAT_TOKEN, config.HIPCHAT_ROOMNAME)
        olark_client = Olark(config.OLARK_USERNAME, config.OLARK_PASSWORD, hipchat_client, config.HIPCHAT_ROOMNAME)

        while True:
            # monitor if there is a participant in the HipChat room
            participants = hipchat_client.get_participants()
            # get the olark client state
            olark_state = olark_client.state.current_state()

            # if participants and olark client is not connected
            if participants and olark_state != "connected":
                # connect it
                if olark_client.connect(("olark.com", 5222)):
                    olark_client.process()

            # if no participant, disconnect olark client
            elif not participants and olark_state == "connected":
                olark_client.disconnect()

            # wait to check again Hipchat participants
            time.sleep(self.sleep_delay)

if __name__ == '__main__':
    client = OlarkHipchat(config.HIPCHAT_SLEEPDELAY)
    client.start()
