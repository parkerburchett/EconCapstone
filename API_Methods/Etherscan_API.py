# https://info.etherscan.com/api-return-errors/
# "Powered by Etherscan.io APIs"  I need to put this somewhere in the final project.

# limited by 5 calls / second per ip with a valid API key. They keys are free.

import json
import requests
from utils import Data_Cleaning

my_json = open(r'C:\Users\parke\Documents\GitHub\EconCapstone\API_Methods\etherScan_apiKey.json') # this gets my private API key for Ethermine.org.
etherscan_api_key =json.load(my_json)['key'] # broken.


my_json.close()
# these are some wallet addresses to test on
ethan = '0xCeB4d0CA821420Cf2553b9e244F6B52364613F94'
big_random_miner = '0xdd619667be721974a21b22bf5e7d54e51adf9c01'
ethermine_wallet = '0xea674fdde714fd979de3edf0f56aa9716b898ec8'


# you need to write a method to stitch these together to call outside of the method.

def get_normal_transactions_command(miner_address, start_block=0, end_block=99999999):
    """
        This generates the proper format to query Etherscan.io for the transactions between two blocks

    :param miner_address: The Ethereum wallet address of the miner you want to get transaction records for
    :param start_block: Default=0
    :param end_block:  Default =99999999 the last block
    :return: The Etherscan.io API command to get the record of the normal('transactions')
    """
    command = 'https://api.etherscan.io/api?module=account&action=txlist&address={}' \
              '&startblock={}&endblock={}&sort=asc&apikey={}'.format(miner_address,
                                                                     start_block,
                                                                     end_block,
                                                                     etherscan_api_key)

    return command

def get_data_from_command(command):
    """
        This makes the command to the etherscan.io API.
        Later you might want to add error correction to the request
    :param command: This is a string of the request of the command to ask the etherscan.io API for
    :return: my_data: a list that represents the data queried from the etherscan.io API.
    """

    response = requests.get(command) # time controls are handled else where
    my_dict = json.loads(response.text)
    return my_dict['result']



def parse_normal_transactions(transaction_list):
    """
        This takes the list of 'normal' transactions and rewrites into a list of tuples that is easy to write to a file.
        In theory you could also use this to update a sql server or another kind of database.

    :param transaction_list: A list of 'normal transactions from the etherscan.io API.

    :return:
        simple_transactions: a list of tuples storing (to_address, from_address, Block number, DateTime, Value in Ether)
                                      Data types are: (String, String, int, string, float)
    """
    simplified_transactions =[]

    # trans is a dictionary object
    for trans in transaction_list:
        to_address = trans['to']
        from_address = trans['from']
        block_number = int(trans['blockNumber'])
        # trans['value'] gets the value in.
        value_in_ether = Data_Cleaning.convert_wei_to_ether(trans['value'])
        datetime_of_trans = str(Data_Cleaning.convert_unix_to_standard_date(trans['timeStamp']))
        simplified_transaction = (to_address,
                                  from_address,
                                  block_number,
                                  datetime_of_trans,
                                  value_in_ether)

        simplified_transactions.append(simplified_transaction)

    return simplified_transactions



def write_transactions_to_csv(simplified_transactions, filename='record_of_transactions.csv'):
    """
        Save the simplified transactions to a csv file.
    :param simplified_transactions: a list of tuples from parse_normal_transactions()
    :param filename: where you want to write the data to
    :return: Nothing
    """
    with open(filename,'w') as out:
        out.write('to_address, from_address, block_number, datetime, amount_ether\n')
        for s in simplified_transactions:
            out.write(str(s)+'\n')
def tester():
    command = get_normal_transactions_command(miner_address=ethermine_wallet)
    data = get_data_from_command(command)
    simplified_transactions = parse_normal_transactions(data)
    write_transactions_to_csv(simplified_transactions)
    print('fin')


def get_normal_transaction(miner_address, start_block=0, end_block=99999999):
    """

    :param miner_address: A wallet Address
    :param start_block: block to start at
    :param end_block: the last block to consider
    :return: a list of tuples representing the transactions for this block between the start_block and end_blokc
    """

    command = get_normal_transactions_command(miner_address, start_block,end_block)
    data = get_data_from_command(command)
    return parse_normal_transactions(data)


def get_to_from_addresses(miner_address, start, end):
    """
        Get all the wallets that have touched this wallet between start and end

    :param miner_address:
    :param start: the block to start at
    :param end: the end block
    :returnaddress_list:  a list of all the addresses that involve this wallet between the start and end blocks
    """
    command = get_normal_transactions_command(miner_address,start_block=start,end_block=end)
    data = get_data_from_command(command)
    address_list = []
    for trans in data:
        to_address = trans['to']
        from_address = trans['from']
        address_list.append(to_address)
        address_list.append(from_address)

    return address_list