"""
This program takes in a .csv file from etherscan.io and write the addresses to Miner_address.csv

You will want to find a way to get a large representative sample for


You can use that list to iterate through etherscan.io to get income statements and ethermine, to get numworkers.


"""

out  = open('Miner_address.csv','w')
with open (r'dec25_5000_transactions.csv', 'r') as file:
    lines = file.readlines()
    for line in lines[1:]: # skip the first line.
        split_lines = line.split(sep=',', maxsplit=16)
        out.write(split_lines[5]+'\n')

out.close()
