import re

from util import hook, http, format
from urllib2 import HTTPError, urlopen

from bs4 import BeautifulSoup

api_prefix = "http://www.wikihow.com/"
search_url= api_prefix + "wikiHowTo?search="

@hook.command('how')
def how(inp):
	try:
	    doc = http.get_html(search_url + inp)
	except HTTPError:
		return 'error fetching results'
	
	try:
		url_result = doc.find_class('result_link')[0]
	except IndexError:
		return 'WikiHow - no results found'
	url_link= url_result.xpath("//*[@id='searchresults_list']/div[2]/div[2]/a/@href")
	result_url='http:'+str(url_link[0])
	
	soup= BeautifulSoup(urlopen(result_url),'html.parser')
	return u"\x02Title:\x02 " + soup.title.text + "  " + result_url