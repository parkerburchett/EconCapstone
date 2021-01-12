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
    standard_date = datetime.datetime.fromtimestamp(unix_time).date() # I only care about the date. I am choosing to ingore data about the time
    return standard_date

def convert_hashes_to_mega_hashes(hashes):
    mega_hashes = float(hashes) / math.pow(10, 6) # there are a million 10^6 hashes in a mega hash
    return  mega_hashes

def convert_Gwei_to_ether(amount_Gwei):
    amount_ether = float(amount_Gwei) / math.pow(10, 9) # there are 10^9 wei in an ether.
    return amount_ether
