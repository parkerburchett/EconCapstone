

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