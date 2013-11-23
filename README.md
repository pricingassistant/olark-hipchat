# Olark - Hipchat


## Features

- Connect to Olark via XMPP
- Use the Hipchat REST API
- Monitor a Hipchat room if a person is connected
- Connect to Olark if one person is connected
- Disconnect from Olark if nobody is connected to Hichat
- Transfer Olark users messages to Hipchat with a notification sound and a link to go to Olark chat


## How to use it

### Install

	$ git clone https://github.com/pricingassistant/olark-hipchat.git
	$ cd olark-hipchat
	$ git checkout dev
	$ pip install -r requirements.txt


### Config

Copy src/config-example.py to src/config.py

	$ cp src/config-example.py src/config.py

Create your HipChat API Token (https://hipchat.com/admin/api) with an admin type

Set it in src/config.py (HIPCHAT_TOKEN)

Change the room name where to send Olark messages (HIPCHAT_ROOMNAME)

Change the Olark username and password (OLARK_USERNAME, OLARK_PASSWORD)


### Execute

	$ python src/olark-hipchat.py
