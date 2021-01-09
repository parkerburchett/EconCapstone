"""
This takes a .json object from the API and writes it out neatly to a .csv file

https://etherscan.io/address/0xCeB4d0CA821420Cf2553b9e244F6B52364613F94
This is ethan's miner.

Do this since you knwo what the values should be

https://etherscan.io/apis

The command to get the json file from the api is


https://api.etherscan.io/api?module=account&action=txlist&address=0xCeB4d0CA821420Cf2553b9e244F6B52364613F94&startblock=0&endblock=99999999&sort=asc&apikey=3KKNT8U3S4Q44UUVFNCD2DSUUBF8H29J5F


This ought to be the same as
https://etherscan.io/address/0xCeB4d0CA821420Cf2553b9e244F6B52364613F94

For whatever reason the 'value' dict object is different than the values
I know they point at the same account

Another option
https://api.etherscan.io/api?module=account&action=txlist&address=0xCeB4d0CA821420Cf2553b9e244F6B52364613F94&startblock=0&endblock=99999999&page=1&offset=10&sort=asc&apikey=3KKNT8U3S4Q44UUVFNCD2DSUUBF8H29J5F


This is not working and I don't know why


"""

import json

my_json = open('fromAPI.json')
trans =json.load(my_json)

single = trans['result']
my_json.close()

s =single[6]


print('fin')