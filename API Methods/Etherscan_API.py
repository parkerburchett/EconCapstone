# https://info.etherscan.com/api-return-errors/
# "Powered by Etherscan.io APIs"  I need to put this somewhere in the final project.

# limited by 5 calls / second per ip with a valid API key. They keys are free.

import json
import requests
from utils import Data_Cleaning

my_json = open('etherScan_apiKey.json') # this gets my private API key for Ethermine.org.
etherscan_api_key =json.load(my_json)['key']
my_json.close()

ethan = '0xCeB4d0CA821420Cf2553b9e244F6B52364613F94'
big_random_miner = '0xdd619667be721974a21b22bf5e7d54e51adf9c01'
ethermine_wallet = '0xea674fdde714fd979de3edf0f56aa9716b898ec8'

def get_normal_transactions_command(miner_address, start_block=0, end_block=99999999):
    command = 'https://api.etherscan.io/api?module=account&action=txlist&address={}' \
              '&startblock={}&endblock={}&sort=asc&apikey={}'.format(miner_address,
                                                                     start_block,
                                                                     end_block,
                                                                     etherscan_api_key)
    # the default command in the API  it should work
    #https: // api.etherscan.io / api?module = account & action = txlist & address = 0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae & startblock = 0 & endblock = 99999999 & page = 1 & offset = 10 & sort = asc & apikey = YourApiKeyToken    return command

    return command

def get_data_from_command(command):
    """
    :param command: This is a string of the request of the command
    :return: a dic
    """
    response = requests.get(command)
    my_dict = json.loads(response.text)
    my_data = my_dict['result']
    return my_data


def parse_normal_transactions(transaction_list):
    """
        This takes the list of transactions and rewrites them in a more clear way for

    :param transaction_list: A list of 'normal transactions from the etherscan.io API.

    :return:
        simple_transactions: an Array of tuples storing (to_address, from_address, Block number, DateTime, Value in Ether)
    """
    simplified_transactions =[]

    for trans in transaction_list:
        to_address = trans['to']
        from_address = trans['from']
        block_number = int(trans['blockNumber'])
        # trans['value'] gets the value in wei for this transaction.
        value_in_ether = Data_Cleaning.convert_wei_to_ether(trans['value'])
        datetime_of_trans = str(Data_Cleaning.convert_unix_to_standard_date(trans['timeStamp']))
        simplified_transaction = (to_address,
                                  from_address,
                                  block_number,
                                  datetime_of_trans,
                                  value_in_ether)

        simplified_transactions.append(simplified_transaction)

    return simplified_transactions


def write_transactions_to_csv(simplified_transactions):
    with open('record_of_transactions.csv','w') as out:
        out.write('to_address, from_address, block_number, datetime, amount_ether\n')
        for s in simplified_transactions:
            out.write(str(s)+'\n')



def tester():
    command = get_normal_transactions_command(miner_address=big_random_miner)
    data = get_data_from_command(command)
    simplified_transactions = parse_normal_transactions(data)
    write_transactions_to_csv(simplified_transactions)


tester()