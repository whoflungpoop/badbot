import re
import time

from util import hook, http, format, colorformat

trigger_imgay_re= (r'(\bI(\')?(\s)?a?m gay)', re.I)
mychar = u'\u5350'

@hook.regex(*trigger_imgay_re)
@hook.command
def imgay(inp):
   return imgay_color(inp)

def imgay_color(inp=None):
	msg = unicode(mychar + 'same' + mychar)
	colorMsg = colorformat.rainbow6(msg)
	return( format.bold( colorMsg.replace(',16',',1') ) )