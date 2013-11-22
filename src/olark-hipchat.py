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
        hipchat_client = HipChat(config.HIPCHAT_TOKEN, config.HIPCHAT_ROOMNAME)
        olark_client = Olark(config.OLARK_USERNAME, config.OLARK_PASSWORD, hipchat_client, config.HIPCHAT_ROOMNAME)

        while True:
            participants = hipchat_client.get_participants()
            olark_state = olark_client.state.current_state()

            if participants and olark_state != "connected":
                if olark_client.connect(("olark.com", 5222)):
                    olark_client.process()

            elif not participants and olark_state == "connected":
                olark_client.disconnect()

            time.sleep(self.sleep_delay)

if __name__ == '__main__':
    client = OlarkHipchat(config.HIPCHAT_SLEEPDELAY)
    client.start()
