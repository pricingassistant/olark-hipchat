import gevent.monkey
gevent.monkey.patch_all()
import time
import logging
import signal
import gevent
import gevent.queue

from expiringdict import ExpiringDict
from sleekxmpp import ClientXMPP
from slacker import Slacker

import config


class OlarkClient(ClientXMPP):

  def __init__(self, queue, username, password, **kwargs):
    super(OlarkClient, self).__init__(queue, username, password, **kwargs)
    self._app_queue = queue
    self.add_event_handler("session_start", self.operator_is_here)
    self.add_event_handler("message", self.visitor_send_message)

  def operator_is_here(self, event):
    """overide an existing method"""
    self.send_presence()
    self.get_roster()

  def get_username(self, from_user):
    from_user = str(from_user)
    return self.client_roster[from_user].get("name") or from_user

  def visitor_send_message(self, message):
    username = self.get_username(message["from"])
    self._app_queue.put((username, message.get("body", "")))


class Application(object):

  def __init__(self):
    self.queue = gevent.queue.Queue(maxsize=10)  # maybe Pricing is on tv?
    self.quota = ExpiringDict(max_length=30, max_age_seconds=config.SLACK_NOTIFICATION_INTERVAL)

    self.slack = Slacker(config.SLACK_TOKEN)
    self.olark = OlarkClient(self.queue, config.OLARK_USERNAME, config.OLARK_PASSWORD)  # Will send events

    self.greenlets = []
    self.running = False

  def register_signals(self):
    signal.signal(signal.SIGINT, self.stop)

  def run(self):
    self.greenlets.add(gevent.spawn(self.greenlet_slack_notifier))

    self.register_signals()
    self.running = True

    olark_connected = False

    while self.running:
      channel_members = self.slack.channels.info(config.SLACK_CHANNEL)["members"]
      connected_chat_users = self.slack.users.list(presence=True)
      connected_channel_users = list(set(channel_members) & set(connected_chat_users))

      if connected_channel_users and not olark_connected:
        logging.info("Users found on Slack, connect to Olark..")
        if self.olark.connect(("olark.com", 5222)):
          self.olark.process()
          olark_connected = True

      elif not connected_channel_users and olark_connected:
        logging.info("No more users on Slack, disconnect from Olark..")
        self.olark.disconnect()
        olark_connected = False

      time.sleep(config.SLACK_PRESENCE_INTERVAL)

    if olark_connected:
      self.olark.disconnect()

  def stop(self):
    self.running = False
    self.olark.stop()
    gevent.joinall(self.greenlets)

  def greenlet_slack_notifier(self):
    while not self.queue.empty():
      username, message = self.queue.get()

      last_notify = self.quota.get(username)

      if last_notify:
        logging.warning("notification already sended for user '%s' over the last %.2f seconds." % (username, time.time() - last_notify))
        continue

      message = "*%s:* %s -> %s" % (username, message, config.OLARK_WEBSERVICE_URL)

      self.slack.chat.post_message(config.SLACK_CHANNEL, message, user=config.SLACK_USERNAME)
      self.quota[username] = time.time()


app = Application()


if __name__ == "__main__":

  app.run()
