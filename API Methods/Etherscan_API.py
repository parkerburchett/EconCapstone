# https://info.etherscan.com/api-return-errors/
# "Powered by Etherscan.io APIs"  I need to put this somewhere in the final project.

# limited by 5 calls / second per ip with a valid API key. They keys are free.

import json
import requests
from utils import Data_Cleaning

my_json = open('etherScan_apiKey.json')
etherscan_api_key =json.load(my_json)['key']
my_json.close()

ethan = 'CeB4d0CA821420Cf2553b9e244F6B52364613F94'
big_random_miner = '969aE8B1708E825570a1bBF4C9C7D2FC7382BadD'



def get_normal_transactions_command(miner_address, start_block=0, end_block=99999999):
    command = 'https://api.etherscan.io/api?module=account&action=txlist&address={}' \
              'bae&startblock={}&endblock={}&sort=asc&apikey={}'.format(miner_address,
                                                                             start_block,
                                                                             end_block,
                                                                             etherscan_api_key)
    # the default command in the API  it should work
    command = 'https://api.etherscan.io/api?module=account&action=txlist&address=0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae&startblock=0&endblock=99999999&sort=asc&apikey={}'.format(etherscan_api_key)

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
    simple_transactions =[]
    for trans in transaction_list:
        raw_value = trans['value'] # you only need to consider the first 17 digits I think, Am unsure.
        trans_hash = trans['hash']
        gas_used = trans['gasUsed']
        if(raw_value!= '0'):
            print('rawValue: {},Gas_used {}, trans: {}'.format(raw_value, gas_used,trans_hash,))
        # in theory the correct answer ought to be
        # 0.012453613379231 Ether
        # print('fin')
        # if float(raw_value) > 0: # this prevents needless work. You are ignoring all 'normal' transactions with no value ==0
        #     to_address = trans['to']
        #     from_address = trans['from']
        #     date = Data_Cleaning.convert_unix_to_standard_date(trans['timeStamp']) # untested.
        #     simple_trans = (to_address,from_address,raw_value,date)
        #     simple_transactions.append(simple_trans)

    return simple_transactions

def tester():
    command = get_normal_transactions_command(ethan)
    data = get_data_from_command(command)
    cleaned_transactions = parse_normal_transactions(data)

    print(cleaned_transactions)

tester()