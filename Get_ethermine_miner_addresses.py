# this is designed to get all (or at least as many as I can) of the~90k. Wallets at ethermine.org
#
#
# For jan 1-jan 8



#pseudocode

# figure out the earilest block on jan 1
    # jan_start_block

# fiure out laest block on jan
    # jan_end_block

#using EtherscanAPI.get_normal_transactions_command()

# step through every block in a for loop between jan_start_block and jan_end_block.

# in a csv file record every single to_address that meets the criteria

# it is sending ether. from ethermine and to a wallet. value !=0.

# There should be a way to only get the unique values from that list. set() would be the simplest.

# outside of the for-loop track the addresses in a list.

# sleep(1 second) every 5 calls. num_blocks to check /5 = number of seconds this will take.

from API_Methods import Etherscan_API


# after you let that run. you should have a very long list of wallet addresse that were sent ether by etherum in that week time frame.

# wrap it all in a date time so you have an Idea of how long it will take.


# you can do this again later to get a better idea of the time constraints.

# IE you could use this method to get a snap shot of everyone who is mining at ethermine between any two arbritay dates.


# if it is not that high of a time cost you can get lots of snapshots of the miners at ethermine.
# this will let you see the old miners and the new miners.





from API_Methods import Etherscan_API
import time

# these number are estimates. It should capture most of the transactions within this window.

# the dominaitng tiem cost is the sleep(1). ths


def main():

    # this is just to scrape a large number of addreses that are from wallets on ethermine.org
    jan_start_block = 11570268 - 100000 # the -100,000 is to get a large margin
    jan_end_block = 11616099


    num_blocks = int(jan_end_block - jan_start_block)

    ethermine_wallet = '0xea674fdde714fd979de3edf0f56aa9716b898ec8'
    # this is the address of the main source of the payouts

    out = open('ethermine_wallets_generated.cvs','w')
    all_addresses = []
    for i in range(0,num_blocks,1000):
        time.sleep(.2) # this is to not get stopped by API call limit you need to wait a second for 5 calls.
        # you might be able to walk thorugh each N block chunk. depending on the number of calls to each block.
        # as long as it is less than 10000 trans in a single block. That would speed it up by a lot.
        local_start = jan_start_block+i
        local_end = local_start+1000

        temp_addresses = Etherscan_API.get_to_from_addresses(ethermine_wallet,local_start,local_end)

        print('there were this many unique addresses between on that touched ethermine.org {} and {}: {}'.format(local_start, local_end, len(temp_addresses)))
        wallets_as_set = set(temp_addresses)
        temp_addresses = list(wallets_as_set)
        all_addresses.extend(temp_addresses) # untested
        a_set = set(all_addresses)
        all_addresses = list(a_set)
        print('there are currently {} unique Addresses'.format(len(all_addresses)))

    for s in all_addresses:
        out.write(s+'\n')


main()