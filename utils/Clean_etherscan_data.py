from datetime import datetime

# this takes in the price data from etherscan.io and puts it into a cleaner format to work with in pyspark


def clean_price_data():
    with open(r'C:\Users\parke\Documents\GitHub\EconCapstone\datasets\export-EtherPrice.csv', 'r') as input:
        with open("clean_price_data.csv", 'w') as out:
            lines = input.readlines()
            lines.pop(0)
            out.write('month_year,Value\n')
            for line in lines:
                cur_line = line.split(',',3)
                unix_time = int(cur_line[1].replace('"',''))
                month_year = str(datetime.fromtimestamp(unix_time))[:7]
                Value = round(float(cur_line[2].replace('"','')),2)
                out.write('{},{}\n'.format(month_year,Value))

def clean_network_hashrate():
    with open(r'C:\Users\parke\Documents\GitHub\EconCapstone\datasets\export-NetworkHash.csv', 'r') as input:
        with open("clean_Network_Hash.csv", 'x') as out:
            lines = input.readlines()
            out.write('year_month,HashRate_(GH/s)\n')
            for line in lines[1:]:
                cur_line = line.split(',')
                unix_time = int(cur_line[1].replace('"', '')) # remove spurious double quotes
                year_month = str(datetime.fromtimestamp(unix_time))[:7]
                gig_hashes_second = float(cur_line[2].replace('"', ''))
                out.write('{},{}\n'.format(year_month,gig_hashes_second))

def clean_new_ethereum():
    # source: https://etherscan.io/chart/ethersupplygrowth
    # I added in excel a simple change (x2-x1) as new_ethersupply
    with open(r'C:\Users\parke\Documents\GitHub\EconCapstone\datasets\export-Ethersupply.csv', 'r') as input:
        with open("clean_new_ETH.csv", 'w') as out:
            lines = input.readlines()
            out.write('year_month,new_ether\n')
            for line in lines[2:]: # ignore the first 2 lines
                cur_line = line.split(',')
                unix_time = int(cur_line[1].replace('"', ''))  # remove spurious double quotes
                year_month = str(datetime.fromtimestamp(unix_time))[:7]
                new_ether = (float(cur_line[3].replace('"','')))
                if year_month != '2015-07': # Exclude July 2015 since you don't have a full month of data fro ti
                    out.write('{},{}\n'.format(year_month,new_ether))



clean_new_ethereum()
