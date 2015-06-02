# shitlist2.py
# @whoflungpoop
# Reqs:
#	- bot must have kick/ban privs (op,admin)
import re
import time
import inspect
from util import hook

@hook.command
def shitlist(inp, chan='', db=None):
	'.shitlist <host> <filter> [kickmsg] -- kick/ban client at <host> for any privmsg containing <filter>, with optional [kickmsg] on kick'
	
	db.execute('create table if not exists '
	'shitlist(chan, host, filter, msg)')
	
def add_sl(db, chan, host, filter, msg):
	match = db.execute('select * from shitlist where '
	'chan = ? and '
	'lower(host) = lower(?) and '
	'lower(filter) = lower(?)',	
	(chan, host, filter)).fetchall()
	if match:
		return 'userhost/filter already exist'
	db.execute('replace into shitlist(chan, host, filter, msg) '
	'values(?,?,?,?)', (chan, host, filter, msg))
	db.commit()
	return ('shitlist entry added.')


	
@hook.singlethread
@hook.event('PRIVMSG')
def shitlistener(param1, kick=None, ban=None, unban=None,input=None, bot=None):
	usr_matches = db.execute('select host, filter, msg from shitlist where '
	'lower(host) = ?',
	(host)).fetchall()
	
	if usr_matches:
	
	return 
	
	
	
	
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