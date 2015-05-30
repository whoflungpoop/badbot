from util import http, hook


@hook.command(autohelp=False)
def bitcoin(inp, say=None):
    ".bitcoin -- gets current exchange rate for bitcoins from BTC-e"
    data = http.get_json("https://btc-e.com/api/2/btc_usd/ticker")
    say("USD/BTC: \x0307{buy:.0f}\x0f - High: \x0307{high:.0f}\x0f"
            " - Low: \x0307{low:.0f}\x0f - Volume: {vol_cur:.0f}".format(**data['ticker']))


@hook.command(autohelp=False)
def doge(inp, say=None):
    ".doge -- gets current exchange rate for 1000DOGE"
    data = http.get_json("https://www.dogeapi.com/wow/v2/?a=get_info")
    k_doge = -1
    if 'data' in data and 'info' in data['data']:
        k_doge = data['data']['info']['doge_usd'] * 1000
    if k_doge != -1:
        say("1000DOGE/USD: \x0307{}\x0f".format('$'+str(round(k_doge,2))))
    else:
        say("dogeapi.com is messed up right now. Try again later.")