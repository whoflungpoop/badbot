import re
import time

from util import hook, http

trigger_mywife_re= (r'\bmy\s(((boy|girl)\s?friend)|\bwife|\b[bg]f)', re.I)


@hook.regex(*trigger_mywife_re)
@hook.command
def mywife(inp):
  return 'lol, cuck'