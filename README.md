### badbot - a bad bot
Fork of yosbot (https://github.com/craisins/yosbot) for #gbs


### INSTALLATION AND SETUP
1. Install Python libs - see [requirements.txt](https://github.com/whoflungpoop/badbot/blob/master/requirements.txt) for list
	- update pip:
	````pip install -U pip````
	- for each lib: 
	````pip install <LIBNAME>````
2. (<i>optional</i>) Register Bot Nick
	- connect to IRC as intended nick
	- register with nickserv:
	````/ns register <PASSWORD> <EMAIL>````
3. Modify Config File
	- rename [configSample](https://github.com/whoflungpoop/badbot/blob/master/configSAMPLE) to ````config````
	- set IRC nick (connections.local irc.nick)
	- (<i>if nick registered</i>) set password (connections.local irc.nickserv_password)
	- add comic path (local directory where generated comics will be stored)
	- fill in other values (i.e. API keys) as needed
4. Obtain API keys
	1. Google Search/Youtube (.g, .gis, .yt)
		- create project at https://console.developers.google.com/
		- enable APIs:
			- Custom Search API
			- Youtube Data API v3
		- generate CLIENT key for PUBLIC/OPEN API **not OAuth**
		- insert key into config: (api_keys.google)
	2. Giphy
	3. Twitter
	4. WolframAlpha
	5. Imgur
	






