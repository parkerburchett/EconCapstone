# https://ethermine.org/api/miner
import requests
import json

miner ='CeB4d0CA821420Cf2553b9e244F6B52364613F94'


# Payouts /miner/:miner/payouts

endpoint ='https://api.ethermine.org'

get_payouts_ethermine = '{}/miner/:{}/payouts'.format(endpoint,miner,miner)

get_main ='https://api.ethermine.org/poolstats' # this works.

response = requests.get(get_payouts_ethermine)

print(get_payouts_ethermine)
my_data = json.loads(response.text)

print(my_data)

print(my_data["data"][0])


