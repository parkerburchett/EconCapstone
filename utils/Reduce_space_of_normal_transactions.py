# https://github.com/parkerburchett/EconCapstone/issues/7

"""
    Right now, a large amount of the data is redundant and it can have it's size reduced to make the processing faster.
    I have several files in API_Methods/Raw_data

    that each look like

to_address,from_address,block_number,datetime,amount_ether
0x1f14c8687f345f99c99a5d169ffa153af7b89840,0xea674fdde714fd979de3edf0f56aa9716b898ec8,1191228,2016-03-21 08:42:27,1.11217021245
0x1f14c8687f345f99c99a5d169ffa153af7b89840,0xea674fdde714fd979de3edf0f56aa9716b898ec8,1192191,2016-03-21 12:34:34,1.1279910724985451
0xa63f4afb1812b17bc011cb516bec57e7009641a9,0xea674fdde714fd979de3edf0f56aa9716b898ec8,1192191,2016-03-21 12:34:34,1.4374289301206984
0x3d1c1b034ed3495e962caadcb322e0cefb2d24cb,0xea674fdde714fd979de3edf0f56aa9716b898ec8,1192191,2016-03-21 12:34:34,1.9337634658422986
0xb202d9a6314b1494ac463f152f551f7c1c577843,0xea674fdde714fd979de3edf0f56aa9716b898ec8,1192191,2016-03-21 12:34:34,1.328998299081973
0x3d31a7cdbf1b9952c1c4d567b97c54fc354e6a7b,0xea674fdde714fd979de3edf0f56aa9716b898ec8,1194607,2016-03-21 22:12:53,1.4575460884079077
0xb202d9a6314b1494ac463f152f551f7c1c577843,0xea674fdde714fd979de3edf0f56aa9716b898ec8,1194608,2016-03-21 22:13:04,1.552392599239843



I want to only get the payments from that address for the miners and save it in a smaller format.
PsuedoCode

put it in this format (to, month-year, amount, 6 digits. that would make it accurate down to approx a 10th of a cent per transaction

    for line in lines:
        if line[1] == ethermine_wallet: # only want payments to wallet.
            to = line[0]
            amount = round(float(line[4]),6)
            year_month = str(line[3][:6]) # only get the month and the year. might be [:5]
            simplified_payment = '{},{},{}'.format(
"""

import Data_Cleaning
import csv



# this is at least one of the wallets.4
f2_pool_wallet = '0x829BD824B016326A401d083B33D092293333A830'
sparkpool_wallet = '0x5A0b54D5dc17e0AadC383d2db43B0a0D3E029c4c'  # has 2 million transactions

# source: https://etherscan.io/stat/miner?range=7&blocktype=blocks
mining_hub_pool = '0x3EcEf08D0e2DaD803847E052249bb4F8bFf2D5bB'
zhi_zhu_pool = '0x04668Ec2f57cC15c381b461B9fEDaB5D451c8F7F'
nano_pool = '0x52bc44d5378309EE2abF1539BF71dE1b7d7bE3b5'

def main():
    sparkpool_wallet = '0x5A0b54D5dc17e0AadC383d2db43B0a0D3E029c4c'.lower()  # has 30 million transactions
    ethermine_wallet = Data_Cleaning.get_ethermine_wallet_address()
    input_file = r'C:\Users\parke\Documents\GitHub\EconCapstone\API_Methods\Raw_data\ethermine_normal_transactions.csv'
    with open(input_file, 'r') as input:
        with open('simplified_ethermine_data.csv', mode='w') as output:
            lines = input.readlines() # there are 30 million lines. This only takes a 10 seconds
            output.write('to_address,year_month,amount\n')
            print("There are {} lines in the input document".format(len(lines)))

            for line in lines:
                cur_line = line.split(',',4)
                if cur_line[1].lower() == ethermine_wallet:  # only want payments to wallet.
                    to_address = cur_line[0]
                    amount = round(float(cur_line[4]), 6) # only want 6 significant digits.
                    year_month = str(cur_line[3][:7])  # only get the month and the year
                    reduced_line = '{},{},{}\n'.format(to_address, year_month, amount)
                    output.write(reduced_line)



    with open('simplified_ethermine_data.csv', mode='r') as out_tester:
        lines = out_tester.readlines()
        print('you have  {} lines after simplifying'.format(len(lines)))


        # for an unknown reason this makes 530 more lines. I don't know why that is

main()
# 4 gigs large. started at 4:31 ended at 4:34