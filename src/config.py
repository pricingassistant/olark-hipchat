# -*- coding: utf-8 -*-
import os

HIPCHAT_TOKEN=os.getenv("HIPCHAT_TOKEN")
HIPCHAT_ROOMNAME=os.getenv("HIPCHAT_ROOMNAME") or "Olark"
HIPCHAT_SLEEPDELAY=int(os.getenv("HIPCHAT_SLEEPDELAY") or "3") # 100 request for 5 minutes !

OLARK_USERNAME=os.getenv("OLARK_USERNAME")
OLARK_PASSWORD=os.getenv("OLARK_PASSWORD")
