import random
import re
import time


from util import hook

trigger_onjoin_re=(r'(whoflungpoop|skulldick', re.I);

@hook.regex(*trigger_onjoin_re)
@hook.event("JOIN")
def onjoin(inp):
  return inp + 'hi'