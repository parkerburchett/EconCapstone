# It might make more sense to walk though all_of ethermine transactions


# there are 30 million transactions for ethermine.You can only get 10k Transactions per

import Etherscan_API
from utils import Data_Cleaning
import time
import csv

# the most recent block  11681687

# 1160000 = March er 16 2016

# 1985000 = july 31 2016 A good enough startign point as any.

def write_all_normal_trans_to_a_file():
    """
            Get all of the money sent by ethermine to every address.
            'to_address', 'from_address', 'block_number', 'datetime', 'amount_ether' format
            THe API will start at the start block and return the first 10,000 records.
            This works by writing that to a file and then changing the start block to the last block that the API returned
            There are 30 Million transaction on Ethermine. This should take approx ~3,000 calls.
            This took about 3 hours to get 30 million records
    """


#   https://www.poolwatch.io/coin/ethereum
    ethermine_wallet = Data_Cleaning.get_ethermine_wallet_address()

    # this is at least one of the wallets.4
    f2_pool_wallet = '0x829BD824B016326A401d083B33D092293333A830'
    sparkpool_wallet = '0x5A0b54D5dc17e0AadC383d2db43B0a0D3E029c4c' # has 2 million transactions



    # source: https://etherscan.io/stat/miner?range=7&blocktype=blocks
    # not done
    mining_hub_pool = '0x3EcEf08D0e2DaD803847E052249bb4F8bFf2D5bB'
    zhi_zhu_pool ='0x04668Ec2f57cC15c381b461B9fEDaB5D451c8F7F'
    nano_pool = '0x52bc44d5378309EE2abF1539BF71dE1b7d7bE3b5'

    with open(r'C:\Users\parke\Documents\GitHub\EconCapstone\API_Methods\zhi_zhu_pool_wallet_normal_transactions.csv', 'x', newline='') as out:

        writer = csv.writer(out)

        writer.writerow(['to_address', 'from_address', 'block_number', 'datetime', 'amount_ether'])

        normal_trans = Etherscan_API.get_normal_transaction(zhi_zhu_pool, start_block=0)

        while (len(normal_trans)>0): # while it gives you some transaction data.

            block_to_exclude = normal_trans[-1][2] # the latest block
            normal_trans.pop(-1) # you will always pop this transaction

            while (normal_trans[-1][2] == block_to_exclude): # check if this transaction is on the block you wish to exclude
                normal_trans.pop(-1)

            writer.writerows(normal_trans)
            print('you just wrote {} transactions between blocks {} and {}'.format(len(normal_trans), normal_trans[0][2],normal_trans[-1][2]))
            time.sleep(.2)
            normal_trans = Etherscan_API.get_normal_transaction(ethermine_wallet, start_block=block_to_exclude)


if __name__ == "__main__":
   write_all_normal_trans_to_a_file()