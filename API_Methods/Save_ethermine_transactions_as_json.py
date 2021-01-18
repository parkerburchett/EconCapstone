# It might make more sense to walk though all_of ethermine transactions


# there are 30 million transactions for ethermine.You can only get 10k Transactions per

import Etherscan_API
from utils import Data_Cleaning
import time
import csv

# the most recent block  11681687

# 1160000 = March er 16 2016

# 1985000 = july 31 2016 A good enough startign point as any.

def write_all_ethermine_normal_trans_to_a_file():
    """
            Get all of the money sent by ethermine to every address.
            'to_address', 'from_address', 'block_number', 'datetime', 'amount_ether' format

            THe API will start at the start block and return the first 10,000 records.

            This works by writing that to a file and then changing the start block to the last block that the api gave you.
    :return:
    """

    ethermine_wallet = Data_Cleaning.get_ethermine_wallet_address()

    with open(r'C:\Users\parke\Documents\GitHub\EconCapstone\API_Methods\ethermine_normal_transactions.csv', 'w', newline='') as out:

        writer = csv.writer(out)

        writer.writerow(['to_address', 'from_address', 'block_number', 'datetime', 'amount_ether'])

        normal_trans = Etherscan_API.get_normal_transaction(ethermine_wallet, start_block=0)

        while (len(normal_trans)>0):

            block_to_exclude = normal_trans[-1][2] # the latest block
            normal_trans.pop(-1) # you will always pop this transaction

            while (normal_trans[-1][2] == block_to_exclude):
                print('{}\nHas the same block as {}'.format(normal_trans[-1],block_to_exclude))
                normal_trans.pop(-1)

            writer.writerows(normal_trans)
            print('you just wrote {} transactions between blocks {} and {}'.format(len(normal_trans), normal_trans[0][2],normal_trans[-1][2]))
            time.sleep(1)
            normal_trans = Etherscan_API.get_normal_transaction(ethermine_wallet, start_block=block_to_exclude)


if __name__ == "__main__":
   write_all_ethermine_normal_trans_to_a_file()