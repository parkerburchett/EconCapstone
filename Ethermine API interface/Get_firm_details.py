# https://ethermine.org/api/miner
import requests
import json
import math
from datetime import datetime



# Payouts /miner/:miner/payouts
    #### the : means substitute in your own varibale name, Else write diricetly as is

# # https://ethermine.org/api/miner

# 10^9 Wei =  1 Gwei
# 10&9 Gwei = 1 ether

# to go from base units (Wei into ether * 10^18)

def get_payouts_command(miner_address):
    """

    :param miner_address: the mining address of an etherum miner. This is there wallet address
    :return: the command for the api to return a list of all of the payments (last 100 payments) to this account.
    """
    endpoint = 'https://api.ethermine.org'
    command = '{}/miner/:{}/payouts'.format(endpoint, miner_address)
    return command

def get_workers_command(miner_address):
    endpoint = 'https://api.ethermine.org'
    command = '{}/miner/:{}/workers'.format(endpoint, miner_address)
    return command

def get_data_from_command(command):
    """

    :param command: This is a string of the request of the command
    :return: a dic
    """
    response = requests.get(command)
    my_dict = json.loads(response.text)
    my_data = my_dict['data']
    return my_data

def convert_payouts_into_human_readable(payouts):
    """

    :param payouts: this takes the list of payments from the json object and returns a cleaned version.
    :return: a list of date of payment, amount in either tuples.
    """
    simple_payments =[]
    for p in payouts:
        amount_ether = float(p['amount']) / math.pow(10,18) # go from Wei to ether
        payment_date = datetime.fromtimestamp(p['paidOn']).date() # go from unix time stamp to a date
        simple_payments.append((payment_date,amount_ether))

    return simple_payments # (payment date, amount in ether) tuple



ethan ='CeB4d0CA821420Cf2553b9e244F6B52364613F94'
big_random_miner = '969aE8B1708E825570a1bBF4C9C7D2FC7382BadD'
#
# command = get_payouts_command(big_random_miner)
# my_data =get_data_from_command(command)
# simple_payments = convert_payouts_into_human_readable(my_data)


w_command = get_workers_command(big_random_miner)
list_of_workers =get_data_from_command(w_command)

# {'worker': '0030180db667', 'time': 1610412600, 'lastSeen': 1610412561, 'reportedHashrate': 243666806, 'currentHashrate': 208833333.33333334, 'validShares': 186, 'invalidShares': 0, 'staleShares': 3, 'averageHashrate': 241443672.83950615}
print('fin')
