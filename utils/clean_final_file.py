"""
Despite my best effors there are still data that got into final_data_out.csv that should not exist.

This goes through are removes all of the rows that don't make any sense.

Conditiosns to remove.

If firm_size ==0

if  eth_earned_this_month ==0

if GHs_elasticity ==0 || inf or -inf.


wallet_address	 pool_name	 firm_first_full_month	 firm_size	 firm_age	 month	 eth_earned_this_month	 GHs_elasticity	 prev_month_GHs_value	 prev_prev_month_GHs_value

"""

import csv




def main():
    with open(r'C:\Users\parke\Documents\GitHub\EconCapstone\utils\final_data_out.csv','r', newline='') as raw_file:
        reader = csv.reader(raw_file)
        rows_kept =0
        rows_lost =0
        header = next(reader)
        with open(r'C:\Users\parke\Documents\GitHub\EconCapstone\utils\clean_final_data_out.csv','w', newline='') as out:
            writer = csv.writer(out)
            writer.writerow(header)
            for row in reader:
                cur_line = row
                if cur_line[3] != '0.0' and cur_line[6] != '0.0' and cur_line[7] != '0.0' and cur_line[7] != '-inf'and cur_line[7] != 'inf':
                    writer.writerow(cur_line)
                    rows_kept +=1
                else:
                    rows_lost +=1

    print('fin')
    print(rows_kept)
    print(rows_lost)

main()