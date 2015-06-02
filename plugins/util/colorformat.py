__author__ = 'whoflungpoop'
#   Pre-Defined color patterns for irc color text.

import re
import format

pattern = ([format.RED, format.OLIVE, format.YELLOW, format.LIME_GREEN, format.BLUE, format.PURPLE],
           [format.WHITE, format.WHITE, format.BLACK, format.BLACK, format.WHITE, format.WHITE])
# 6-color rainbow gradient, from red to purple.
def rainbow6(text):
    finalText = u''
    for i, c in enumerate(text):
        finalText.append(format.color(c, (int)(pattern[0][i%6]), (int)(pattern[1][i%6]))
    return(finalText)