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


class ChannelNotFoundError(Exception):
  pass


class OlarkClient(ClientXMPP):

  def __init__(self, queue, username, password, **kwargs):
    super(OlarkClient, self).__init__(username, password, **kwargs)
    self._app_queue = queue
    self.add_event_handler("session_start", self.operator_is_here)
    self.add_event_handler("message", self.visitor_send_message)

  def operator_is_here(self, event):
    """overide an existing method"""
    self.send_presence()
    self.get_roster()

  def get_username(self, from_user):
    from_user = str(from_user)
    return self.client_roster[from_user]["name"] or from_user

  def visitor_send_message(self, payload):
    username = self.get_username(payload["from"])
    message = payload.get("body", "")
    logging.debug("Got an incoming message from '%s': '%r'" % (username, message))
    if config.OLARK_IGNORE_USERS and username not in config.OLARK_IGNORE_USERS:
      self._app_queue.put((username, message))


class Application(object):

  def __init__(self):
    self.queue = gevent.queue.Queue(maxsize=10)
    self.quota = ExpiringDict(max_len=30, max_age_seconds=config.SLACK_NOTIFICATION_INTERVAL)

    self.slack = Slacker(config.SLACK_TOKEN)
    self.olark = OlarkClient(self.queue, config.OLARK_USERNAME, config.OLARK_PASSWORD)

    self.greenlets = []
    self.running = False
    self.channel_id = None

  def register_signals(self):
    signal.signal(signal.SIGINT, self.stop)

  def run(self):
    # get the channel id, usage of name as channel results a channel_not_found.
    for channel in self.slack.channels.list().body["channels"]:
      if channel["name"] == config.SLACK_CHANNEL.strip("#"):
        self.channel_id = channel["id"]

    if not self.channel_id:
      raise ChannelNotFoundError("Cannot found channel named %s" % config.SLACK_CHANNEL)

    self.greenlets.append(gevent.spawn(self.greenlet_slack_notifier))

    self.register_signals()
    self.running = True

    olark_connected = False

    while self.running:
      channel_members = self.slack.channels.info(self.channel_id).body["channel"]["members"]
      connected_chat_users = [i["id"] for i in self.slack.users.list(presence=True).body["members"]]
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

    gevent.joinall(self.greenlets)

  def stop(self):
    self.running = False

  def greenlet_slack_notifier(self):
    while True:
      username, message = self.queue.get()

      last_notify = self.quota.get(username)

      if last_notify:
        logging.warning("notification already sended for user '%s' over the last %.2f seconds" % (username, time.time() - last_notify))
        continue

      message = "*%s:* %s -> %s" % (username, message, config.OLARK_WEBSERVICE_URL)

      self.slack.chat.post_message(self.channel_id, message, username=config.SLACK_USERNAME)
      self.quota[username] = time.time()
      time.sleep(1)


app = Application()


if __name__ == "__main__":
  logging.basicConfig(level=getattr(config, "LOG_LEVEL", logging.INFO))
  app.run()
