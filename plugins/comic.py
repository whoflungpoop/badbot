#comic.py almost entirely by https://github.com/nekosune/WeedBot
#modified for yosbot by craisins

import os
import random
import base64
import requests
import time
import json


from util import hook, http
from random import shuffle
from PIL import Image, ImageDraw, ImageFont

comic_cache = {}
comic_cache_buffer_size = 30

@hook.regex(r'.*')
def comic_cacher(match, nick='', chan='', server=''):
        msg = match.group(0)
        key = (chan, server)
        value = (time.time(), nick, msg)

        if key not in comic_cache:
            comic_cache[key] = []


        if msg.startswith("."):
            return
        if nick == "yosbot":
            return

        comic_cache[key].append(value)
        comic_cache[key] = comic_cache[key][-1*comic_cache_buffer_size:]


@hook.api_key('imgur')
@hook.command
def comic(inp, nick='', input=None, db=None, bot=None, server='', api_key=None):
    #print os.getcwd()
    if len(inp) == 0:
        inp = input.chan
    msgs = comic_cache[(inp, server)]
    sp = 0
    chars = set()

    print msgs

    for i in xrange(len(msgs)-1, 0, -1):
        sp += 1
        diff = msgs[i][0] - msgs[i-1][0]
        chars.add(msgs[i][1])
        if sp > 10 or diff > 120 or len(chars) > 3:
            break

    #print sp, chars
    msgs = msgs[-1*sp:]

    panels = []
    panel = []

    for (d, char, msg) in msgs:
        if len(panel) == 2 or len(panel) == 1 and panel[0][0] == char:
            panels.append(panel)
            panel = []
        if msg.count('\x01') >= 2:
            ctcp = msg.split('\x01', 2)[1].split(' ', 1)
            if len(ctcp) == 1:
                ctcp += ['']
            if ctcp[0]=='ACTION':
                msg='*'+ctcp[1]+'*'
        panel.append((char, msg))

    panels.append(panel)

    fname = ''.join([random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789") for i in range(32)]) + ".jpg"

    make_comic(chars, panels).save(os.path.join(bot.config['comic_path'], fname), quality=100)
    image_path = os.path.join(bot.config['comic_path'],fname)
    headers = {'Authorization': 'Client-ID '+ api_key }
    fh = open(image_path, 'rb');
    base64img = base64.b64encode(fh.read())
    url="https://api.imgur.com/3/upload.json"
    r = requests.post(url, data={'key': api_key, 'image':base64img, 'title':'Comic requested by ' + nick}, headers=headers, verify=False)
    val=json.loads(r.text)

    return val['data']['link']


def wrap(st, font, draw, width):
    #print "\n\n\n"
    st = st.split()
    mw = 0
    mh = 0
    ret = []

    while len(st) > 0:
        s = 1
        #print st
        #import pdb; pdb.set_trace()
        while True and s < len(st):
            w, h = draw.textsize(" ".join(st[:s]), font=font)
            if w > width:
                s -= 1
                break
            else:
                s += 1

        if s == 0 and len(st) > 0: # we've hit a case where the current line is wider than the screen
            s = 1

        w, h = draw.textsize(" ".join(st[:s]), font=font)
        mw = max(mw, w)
        mh += h
        ret.append(" ".join(st[:s]))
        #print st[:s]
        #print
        st = st[s:]

    return (ret, (mw, mh))

def rendertext(st, font, draw, pos):
    ch = pos[1]
    for s in st:
        w, h = draw.textsize(s, font=font)
        draw.text((pos[0], ch), s, font=font, fill=(0xff,0xff,0xff,0xff))
        ch += h

def fitimg(img, (width, height)):
    scale1 = float(width) / img.size[0]
    scale2 = float(height) / img.size[1]

    l1 = (img.size[0] * scale1, img.size[1] * scale1)
    l2 = (img.size[0] * scale2, img.size[1] * scale2)

    if l1[0] > width or l1[1] > height:
        l = l2
    else:
        l = l1

    return img.resize((int(l[0]), int(l[1])), Image.ANTIALIAS)

def make_comic(chars, panels):
    #filenames = os.listdir(os.path.join(os.getcwd(), 'chars'))

    panelheight = 300
    panelwidth = 450

    filenames = os.listdir('plugins/data/comic/characters/')
    shuffle(filenames)
    filenames = map(lambda x: os.path.join('plugins/data/comic/characters', x), filenames[:len(chars)])
    chars = list(chars)
    chars = zip(chars, filenames)
    charmap = dict()
    for ch, f in chars:
        charmap[ch] = Image.open(f)

    #print charmap


    imgwidth = panelwidth
    imgheight = panelheight * len(panels)

    bg = Image.open("plugins/data/comic/backgrounds/beach.jpg")

    im = Image.new("RGBA", (imgwidth, imgheight), (0xff, 0xff, 0xff, 0xff))
    font = ImageFont.truetype("plugins/data/comic/fonts/ComicSansBold.TTF", 14)

    for i in xrange(len(panels)):

        pim = Image.new("RGBA", (panelwidth, panelheight), (0xff, 0xff, 0xff, 0xff))
        pim.paste(bg, (0, 0))
        draw = ImageDraw.Draw(pim)

        st1w = 0; st1h = 0; st2w = 0; st2h = 0
        (st1, (st1w, st1h)) = wrap(panels[i][0][1], font, draw, 2*panelwidth/3.0)
        rendertext(st1, font, draw, (10, 10))
        if len(panels[i]) == 2:
            (st2, (st2w, st2h)) = wrap(panels[i][1][1], font, draw, 2*panelwidth/3.0)
            rendertext(st2, font, draw, (panelwidth-10-st2w, st1h + 10))

        texth = st1h + 10
        if st2h > 0:
            texth += st2h + 10 + 5

        maxch = panelheight - texth
        im1 = fitimg(charmap[panels[i][0][0]], (2*panelwidth/5.0-10, maxch))
        pim.paste(im1, (10, panelheight-im1.size[1]), im1)

        if len(panels[i]) == 2:
            im2 = fitimg(charmap[panels[i][1][0]], (2*panelwidth/5.0-10, maxch))
            im2 = im2.transpose(Image.FLIP_LEFT_RIGHT)
            pim.paste(im2, (panelwidth-im2.size[0]-10, panelheight-im2.size[1]), im2)

        draw.line([(0, 0), (0, panelheight-1), (panelwidth-1, panelheight-1), (panelwidth-1, 0), (0, 0)], (0, 0, 0, 0xff))
        del draw
        im.paste(pim, (0, panelheight * i))

    return im