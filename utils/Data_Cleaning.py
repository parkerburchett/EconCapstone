"""
    This is where I am keeping all the data parsing methods.
"""
import math
import datetime

def convert_wei_to_ether(amount_wei):
    amount_ether = float(amount_wei) / math.pow(10, 18) # there are 10^18 wei in an ether.
    return amount_ether

def convert_unix_to_standard_date(unix_time):
    unix_time = int(unix_time)
    standard_date = datetime.datetime.fromtimestamp(unix_time)
    return standard_date

def convert_hashes_to_mega_hashes(hashes):
    mega_hashes = float(hashes) / math.pow(10, 6) # there are a million 10^6 hashes in a mega hash
    return  mega_hashes

def convert_Gwei_to_ether(amount_Gwei):
    amount_ether = float(amount_Gwei) / math.pow(10, 9) # there are 10^9 wei in an ether.
    return amount_ether

def get_month_year_numbers():
    """
    This is a just a faster way of storing the month names. only looking at the 6 year between 2015 and 2020

    Returns a list of strings reprsenting the months you are interested in.

    """
    return ['2015-1', '2015-2', '2015-3', '2015-4', '2015-5', '2015-6', '2015-7', '2015-8',
            '2015-9', '2015-10', '2015-11', '2015-12', '2016-1', '2016-2', '2016-3', '2016-4',
            '2016-5', '2016-6', '2016-7', '2016-8', '2016-9', '2016-10', '2016-11', '2016-12',
            '2017-1', '2017-2', '2017-3', '2017-4', '2017-5', '2017-6', '2017-7', '2017-8', '2017-9',
            '2017-10', '2017-11', '2017-12', '2018-1', '2018-2', '2018-3', '2018-4', '2018-5', '2018-6',
            '2018-7', '2018-8', '2018-9', '2018-10', '2018-11', '2018-12', '2019-1', '2019-2', '2019-3',
            '2019-4', '2019-5', '2019-6', '2019-7', '2019-8', '2019-9', '2019-10', '2019-11', '2019-12',
            '2020-1', '2020-2', '2020-3', '2020-4', '2020-5', '2020-6', '2020-7', '2020-8', '2020-9',
            '2020-10', '2020-11', '2020-12']

def get_ethermine_wallet_address():
    return '0xea674fdde714fd979de3edf0f56aa9716b898ec8'

