# texts from westeros random image

import re
from urllib2 import HTTPError

from util import hook, http

url_tumblr = 'http://textsfromtheironthone.tumblr.com/random'

@hook.command('got')
def got(inp):
	try:
		doc = http.get_html(url_tumblr)
	except HTTPError:
		return 'error fetching results'

	url_picture = doc.find_class('photo')[0]
	url_raw = url_picture.xpath("/html/body/div[@id='wrapper']/div[@id='main']/div[@id='container']/div[@id='content']/div/div[@class='post-content']/a[1]/img[@class='photo']/@src")
	url_regex = re.search("[^\'\[].+[^\'\]]", str(url_raw))
	return url_regex.group(0)