import re
import time

from util import hook, http, format

trigger_imgay_re= (r'(\bI\'?a?m gay)', re.I)
mychar = u'\u5350'

@hook.regex(*trigger_imgay_re)
@hook.command
def imgay(inp):
   return imgay_color(inp)
#return('same')


def imgay_color(inp):

  
  return format.bold((format.color(mychar,'0', format.RED) +  format.color('s',format.BLACK,'7') +
format.color('a',format.BLACK, format.YELLOW) + 
format.color('m','0', format.GREEN) + format.color('e','0', format.BLUE) + 
format.color(mychar,'0', format.PURPLE)) )
