# this takes a series of .csc.crc files and merges them into a single
# human readable .csv file that represents the data for every miner

# I am using this online conversion tool
#https://www.ezyzip.com/convert-zip-to-csv.html




"""
Pseudocode:

Open the dirictory of all the .csv files after you convert them through
# https://www.ezyzip.com/convert-zip-to-csv.html


Source:
https://www.freecodecamp.org/news/how-to-combine-multiple-csv-files-with-8-lines-of-code-265183e0854/

"""

import os
import glob
import pandas as pd
os.chdir(r'C:\Users\parke\Documents\GitHub\EconCapstone\datasets\temp_to_convert\as_csv')


extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

print(all_filenames)


header = ['year_month',
          'to_address',
          'miner_monthly_eth_revenue',
          'average_eth_market_price',
          'global_average_hashrate',
          'monthly_new_eth',
          'derived_ghs_required_for_one_eth',
          'derived_USD_value_of_ghs',
          'derived_monthly_miner_ghs',
          'derived_miner_monthly_USD_revenue']

combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])

print('you have now read in the files')


combined_csv.to_csv( "full_miner_info.csv", index=False, encoding='utf-8-sig')


print('fin')