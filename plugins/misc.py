import urllib2
import re
import socket
import subprocess
import time

from util import hook, http, urlnorm, timesince
from bs4 import BeautifulSoup

socket.setdefaulttimeout(10)  # global setting

ignored_domains = [
    urlnorm.normalize("youtube.com"),
    urlnorm.normalize("google.com"),
    urlnorm.normalize("twitter.com"),
    urlnorm.normalize("forums.somethingawful.com"),
    urlnorm.normalize("youtu.be")
]


def get_version():
    # p = subprocess.Popen(['git', 'log', '--oneline'], stdout=subprocess.PIPE)
    # stdout, _ = p.communicate()
    # p.wait()

    # revnumber = len(stdout.splitlines())

    # shorthash = stdout.split(None, 1)[0]

    # http.ua_skybot = 'Skybot/r%d %s (http://github.com/rmmh/skybot)' \
    #     % (revnumber, shorthash)

    # return shorthash, revnumber
    return "1.0"


# autorejoin channels
@hook.event('KICK')
def rejoin(paraml, conn=None):
    if paraml[1] == conn.nick:
        if paraml[0].lower() in conn.conf.get("channels", []):
            conn.join(paraml[0])


# join channels when invited
@hook.event('INVITE')
def invite(paraml, conn=None):
    conn.join(paraml[-1])


@hook.event('004')
def onjoin(paraml, conn=None):
    # identify to services
    nickserv_password = conn.conf.get('nickserv_password', '')
    nickserv_name = conn.conf.get('nickserv_name', 'nickserv')
    nickserv_command = conn.conf.get('nickserv_command', 'IDENTIFY %s')
    if nickserv_password:
        conn.msg(nickserv_name, nickserv_command % nickserv_password)
        time.sleep(1)

    # set mode on self
    mode = conn.conf.get('mode')
    if mode:
        conn.cmd('MODE', [conn.nick, mode])

    # join channels
    for channel in conn.conf.get("channels", []):
        conn.join(channel)
        time.sleep(1)  # don't flood JOINs

    # set user-agent
    #ident, rev = get_version()


@hook.regex(r'^\x01VERSION\x01$')
def version(inp, notice=None):
    # ident, rev = get_version()
    notice('\x01VERSION skybot - http://github.com/rmmh/'
           'skybot/\x01')


@hook.regex(r'([a-zA-Z]+://|www\.)[^ ]+')
def urlinput(match, nick='', chan='', db=None, bot=None):
    url = urlnorm.normalize(match.group().encode('utf-8'))
    should_ignore = False
    for domain in ignored_domains:
        temp_url = url.replace('https://', '').replace('http://', '').replace('www.', '')
        if domain in temp_url:
            should_ignore = True
            break
    print url
    if not should_ignore:
        url = url.decode('utf-8')
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        title = soup.title.find(text=True).strip()
        if title != "" and title is not None:
            return u"\x02Title:\x02 {}".format(title)
