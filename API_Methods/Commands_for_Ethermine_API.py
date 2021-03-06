# https://ethermine.org/api/miner
import requests
import json
import math
from datetime import datetime
from utils import Data_Cleaning



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
    :return: the data in the command. This ought to be renamed to work with just payment_data.
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
        amount_ether = Data_Cleaning.convert_wei_to_ether(p['amount']) # might be wrong
        payment_date = Data_Cleaning.convert_unix_to_standard_date(p['paidOn'])
        simple_payments.append((payment_date,amount_ether))

    return simple_payments # (payment date, amount in ether) tuple

def parse_worker_data(workers):
    """
        Converts the list of workers to an array of tuples of 'workerID, average(mH/s), date queried)
    :param workers: a list of worker objects from the etherscan.org API
    :return: a list of (worker_id, avg_Mega_Hashes_per_second, date queried)
    """
    simplified_worker_data =[]
    # this will happen many times, you might large might want to rewrite as list comprehension.
    # I think that the primary limit will be the number of API calls I can make. Not the time cost of the the data.
    for w in workers:
        worker_id = w['worker']
        date_queried= Data_Cleaning.convert_unix_to_standard_date(w['time'])
        avg_Mega_Hashes_per_second = Data_Cleaning.convert_hashes_to_mega_hashes(w['averageHashrate'])
        worker_stats = (worker_id,avg_Mega_Hashes_per_second,date_queried)
        simplified_worker_data.append(worker_stats)

    return simplified_worker_data



ethan ='CeB4d0CA821420Cf2553b9e244F6B52364613F94'
big_random_miner = '969aE8B1708E825570a1bBF4C9C7D2FC7382BadD'

command = get_payouts_command(big_random_miner)
my_data = get_data_from_command(command)
simple_payments = convert_payouts_into_human_readable(my_data)


w_command = get_workers_command(big_random_miner)
list_of_workers =get_data_from_command(w_command)

worker_data = parse_worker_data(list_of_workers)


for w in worker_data[:50]:
    print(w)




print('fin')
