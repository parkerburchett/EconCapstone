from API_Methods import Etherscan_API
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import random
from time import strptime
from utils import Data_Cleaning


ethermine_wallet = '0xea674fdde714fd979de3edf0f56aa9716b898ec8'
big_random_miner = '0xdd619667be721974a21b22bf5e7d54e51adf9c01'
big_miner_2 ='0xddd31343c41ff761e674c5bfd74e043059fcb2d0'
old_miner = '0xdc82b8db4a2198443aa583c00ac54cba7b6d5039'
constant_decrease_miner = '0x72c013330cdfef5c4d8d5880944bc8cd953bd352'

def sum_ether_by_month(income_records: dict) -> list:
    """
        Get the total ether earned each month by this wallet from ethermine.org
    Source:
    # https://stackoverflow.com/questions/43235416/group-tuple-according-to-date-in-python
    :rtype: list
    :param income_records: A list of tuples of (datetime, income in ether from ethermien)
    :return: dict of (date: ether earned that month) for every month that there is income
    """
    months = list(set(['-'.join(item[1].split('-')[:2]) for item in income_records]))
    grouped_data = [[x[0] for x in income_records if '-'.join(x[1].split('-')[:2]) == month]
                    for month in months]

    summation_as_dict = {month: sum(item) for month, item in zip(months, grouped_data)}

    summation_as_list = list(summation_as_dict.items())

    summation_as_list.sort(key=lambda x: x[0]) # sort by month
    return summation_as_list

def sum_ether_by_month_v2(income_records: dict) -> list:
    """
        Get the total ether earned each month by this wallet from ethermine.org.
        between Jan 2015 - Dec 2020.

        This method is better.

    :rtype: list
    :param income_records: A list of tuples of (datetime, income in ether from ethermine.org)
    :return: dict of (date: ether earned that month) for every month that there is income
    """
    months = Data_Cleaning.get_month_year_numbers()

    sum_monthly_income = {}
    for month_year in months:
        sum_monthly_income[month_year]=0.0 # initalize the dictionary

    for income_instance in income_records:
        income_month = income_instance[1][:7]
        # there is a problem with leading 0s on the month. This solves that problem. by removing leading zeros
        if income_month[5] == '0':
            print(income_month)
            start = income_month[:5]
            end = income_month[6:]
            income_month = start+end # reassigned leading zeros problem

        print('you added {} to {}'.format(income_instance[0],income_month))
        try:
            sum_monthly_income[income_month] = sum_monthly_income[income_month] + income_instance[0]
        except:
            print('{} is outside side of the range Jan 2015 - Dec 2020'.format(str(income_instance)))

    return list(sum_monthly_income.items())



def create_bar_plot_income(monthly_income):
    """
        Generate a bar plot for this miner's income
    :param monthly_income:
    A sorted list of tuples representing (month, total ether )
    :return: nothing, shows a graph
    """
    x_val = [x[0] for x in monthly_income]
    y_val = [x[1] for x in monthly_income]
    plt.bar(x_val, y_val)
    plt.xlabel('Month')
    plt.ylabel('Ether')
    plt.xticks(rotation=45)

    plt.title('Ether Per Month Since Start')

    plt.show()



# you need a method that overlays the %change in income with the % change in average monthly price
# also with the previous month high.
# also with the previous-1 month high.

def get_wallet_income_from_ethermine(miner_address,get_date=True):
    command = Etherscan_API.get_normal_transactions_command(miner_address)
    data = Etherscan_API.get_data_from_command(command)
    simplified_transactions = Etherscan_API.parse_normal_transactions(data)
    #simplified_transactions a list of tuples: (to_address, from_address, block_number, datetime, amount_ether)
    income_records =[]
    for s in simplified_transactions:
        if (s[1] == ethermine_wallet) and (s[4] > 0):
            # if the ether came from ethermine.org and its value is greater than 0.
            income = (s[4],s[3])
            income_records.append(income)

    if get_date:
        date_of_first_income = datetime.datetime.strptime(income_records[0][1], '%Y-%m-%d %H:%M:%S')
        monthly_income = sum_ether_by_month_v2(income_records) # form ("2016-3", 2.03252) : date, amount of ether.
        return monthly_income,date_of_first_income
    else:
        return sum_ether_by_month(income_records)

def read_in_wallet_addresses(filename ='ethermine_wallets_generated.csv'):
    """
        Get all of the wallets that have mined from ethermine.org
    :param filename: the location of where you are storing all the wallets that use ethermine.
    :return addreseses: a list of wallets that mine at ethermine
    """
    with open (filename) as file_in:
        addresses = file_in.readlines()
        addresses =[a[:42] for a in addresses] # strip the carriage return
        random.shuffle(addresses)
        return addresses



# this is too slow. I need a faster way of doing this.
def visualize_monthly_income(only_large_firms=False):
    """
    See bar graphs of ether income from miners at ethermine.org
    :return: nothings just shows a graph
    """
    import time

    start = datetime.datetime.now()
    wallets = read_in_wallet_addresses()
    time_since_found_last = datetime.datetime.now()
    counter =0
    for wallet in wallets:
        # you need a way to pop an error if it didn't work

        monthly_income = get_wallet_income_from_ethermine(wallet)
        counter +=1
        if not only_large_firms:
            create_bar_plot_income(monthly_income)
        else:
            # this is a simple way to get the addresses of every wallet.
            # there is no reason to choose this standard over anther one
            first_year_income = [income[1] for income in monthly_income[:12]]

            if sum(first_year_income)>100: # If they made more than a hundred ether in the first year
                time_between = str(datetime.datetime.now()- time_since_found_last)
                print('{} On {} of 90000. ;{}; is a large firm'.format(time_between, counter, wallet))
                time_since_found_last = datetime.datetime.now()
                #create_bar_plot_income(monthly_income)
    print('TotalTime Spent:' +str(datetime.datetime.now()-start))

def record_monthly_income_by_wallet():
    """
            Take the list wallets and write to a file
            (wallet address, date of first income, 72[] for the ether earned in every month since
            jan 2015)
    :return:
    """

    wallets = read_in_wallet_addresses()
    for wallet in wallets:
        monthly_income, date_of_first_income = get_wallet_income_from_ethermine(wallet,get_date=True)

    print('stub')


def generate_list_of_month_ids():
    """
        This write the months-Year in the form of 2020-6 to month_names.csv
    """
    # Source: https://stackoverflow.com/questions/34898525/generate-list-of-months-between-interval-in-python
    all_months = pd.date_range('2015-1-1', '2020-12-31',
                  freq='MS').strftime("%Y-%b").tolist()

    with open("month_names.csv", 'w') as month_record:
        for m in all_months:
            year, mon = m.split('-')[0], m.split('-')[1]
            mon_as_num = strptime(mon,'%b').tm_mon # convert to months as number
            to_write = '{}-{}\n'.format(year,mon_as_num)
            print(to_write)
            month_record.write(to_write)

def get_month_year_numbers():
    """
    This is a just a faster way of storing the month names. since it does not change
    :return:
    """
    return ['2015-1', '2015-2', '2015-3', '2015-4', '2015-5', '2015-6', '2015-7', '2015-8',
            '2015-9', '2015-10', '2015-11', '2015-12', '2016-1', '2016-2', '2016-3', '2016-4',
            '2016-5', '2016-6', '2016-7', '2016-8', '2016-9', '2016-10', '2016-11', '2016-12',
            '2017-1', '2017-2', '2017-3', '2017-4', '2017-5', '2017-6', '2017-7', '2017-8', '2017-9',
            '2017-10', '2017-11', '2017-12', '2018-1', '2018-2', '2018-3', '2018-4', '2018-5', '2018-6',
            '2018-7', '2018-8', '2018-9', '2018-10', '2018-11', '2018-12', '2019-1', '2019-2', '2019-3',
            '2019-4', '2019-5', '2019-6', '2019-7', '2019-8', '2019-9', '2019-10', '2019-11', '2019-12',
            '2020-1', '2020-2', '2020-3', '2020-4', '2020-5', '2020-6', '2020-7', '2020-8', '2020-9',
            '2020-10', '2020-11', '2020-12']

monthly_income, date_first_income = get_wallet_income_from_ethermine(big_random_miner,True)

create_bar_plot_income(monthly_income)

