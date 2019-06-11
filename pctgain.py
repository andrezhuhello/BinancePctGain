import json
import time

from cryptowrapper import Binance

path_to_keyfile = '../binance_keys.txt'

# path_to_keyfile default: assumes keyfile is in parent dir
with open(path_to_keyfile, "r") as f:
    binance_key = f.readline().strip()
    binance_secret = f.readline().strip()
    # optional_test = f.readline().strip()

client = Binance(api_key=binance_key, api_secret=binance_secret)

# get info
print(client.ticker_price_GET(symbol="MATICBTC")['price'])

timestamp=int(round(time.time()*1000))
print(timestamp)


print(client.account_trades_GET(symbol="MATICBTC", timestamp=timestamp))


resp = client.account_GET(timestamp=timestamp)
# print(resp)
balances = resp['balances']
print(balances)
coins = []
for balance in balances:
    tkr = balance['asset']
    free = float(balance['free'])
    locked = float(balance['locked'])
    if free>0 or locked>0:
        print(f"{tkr}:\t\t{free} (Free)\t\t{locked} (Locked)")
        coins.append(balance)

tradelist = []
quoted_currency = "BTC"
for coin in coins:
    print(coin)
    tkr = coin['asset']
    if tkr == "BTC":
        continue
    trades = client.account_trades_GET(symbol=f"{tkr}BTC", timestamp=timestamp)
    print(trades)
    if "Invalid symbol" in trades:
        print(f"Skipped!: {tkr}")
        continue
    tradelist.append(trades)
print(tradelist)