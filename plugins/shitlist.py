# shitlist.py
# @whoflungpoop
# Reqs:
#	- bot must have kick/ban privs (op,admin)
import re
import time
import inspect
from util import hook

@hook.singlethread
@hook.event('*')
def shitlist(param1, kick=None, ban=None, unban=None,input=None, bot=None):
	for rule in bot.config.get('shitlist', []):
		if re.search(rule['re'],input.msg, flags=re.IGNORECASE) is not None:
			if re.search(rule['user'], input.host, flags=re.IGNORECASE) is not None:
				do_kick = rule.get('kick', 0)
				ban_length = rule.get('ban_length',0)
				reason = rule.get('msg')
				if (float)(ban_length) != 0:
					ban()
				if do_kick:
					kick(reason=reason)
				elif 'msg' in rule:
					reply(reason)
				if (float)(ban_length) > 0:
					time.sleep((float)(ban_length))
					unban()	