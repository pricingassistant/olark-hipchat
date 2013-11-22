


# How to use it

## Install

	$ git clone https://github.com/pricingassistant/olark-hipchat.git
	$ cd olark-hipchat
	$ git checkout dev
	$ pip install -r requirements.txt


## Config

- Create your HipChat API Token (https://hipchat.com/admin/api) with an admin type
- Set it in src/config.py (HIPCHAT_TOKEN)
- Change the room name where to send Olark messages (HIPCHAT_ROOMNAME)
- Change the Olark username and password (OLARK_USERNAME, OLARK_PASSWORD)


## Execute

	$ python src/olark-hipchat.py
