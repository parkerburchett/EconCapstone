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



# after you let that run. you should have a very long list of wallet addresse that were sent ether by etherum in that week time frame.

# wrap it all in a date time so you have an Idea of how long it will take.


# you can do this again later to get a better idea of the time constraints.

# IE you could use this method to get a snap shot of everyone who is mining at ethermine between any two arbritay dates.


# if it is not that high of a time cost you can get lots of snapshots of the miners at ethermine.
# this will let you see the old miners and the new miners.










ethermine_wallet = '0xea674fdde714fd979de3edf0f56aa9716b898ec8'