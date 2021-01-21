from datetime import datetime

# this takes in the price data from etherscan.io and puts it into a cleaner format to work with in pyspark


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
