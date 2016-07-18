#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Queue
import signal
import time
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__)))

import config
from olarkclient import Olark
from threading import Thread
from slacker import Slacker

logging.basicConfig(level=logging.ERROR)


class OlarkSlack(Thread):

  def __init__(self, sleep_delay, slack_client, olark_client):
    super(OlarkSlack self).__init__()
    self.sleep_delay = sleep_delay
    self.slack_client = slack_client
    self.olark_client = olark_client

    self.running = True


  def run(self):
    while self.running:
      participants = self.slack_client.list(presence=True)
      olark_state = self.olark_client.state.current_state()

      print "Slack operators: %s | Olark state: %s" % (participants, olark_state)

      if participants and olark_state != "connected":
        print "Disconnecting for olark"

if __name__ == "__main__":

  queue = Queue.Queue(maxsize=0)
  slack_client = Slacker()