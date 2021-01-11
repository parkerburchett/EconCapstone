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


https://ethplorer.io/



"""


# proper command https://api.ethplorer.io/getAddressTransactions/0xb297cacf0f91c86dd9d2fb47c6d12783121ab780?apiKey=freekey
# there are limits on the amount you can query from this. I might need to use a larger one once.
# https://docs.ethplorer.io/monitor?from=apiDocs#section/Balances-and-rawBalances-fields-explanation/balances-in-getPoolLastOperations


# you can do things like timestamp=1514764800 to get all stuff since 2018
#timestamp=1483228800 = unix time for jan 1 2017


import json

my_json = open('ethan_via_ethplorer.json')
trans =json.load(my_json)
my_json.close()

print('fin')