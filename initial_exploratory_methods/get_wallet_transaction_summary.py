from API_Methods import Etherscan_API
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import random
from time import strptime
from utils import Data_Cleaning


# you need a method that overlays the %change in income with the % change in average monthly price
# also with the previous month high.
# also with the previous-1 month high.

ethermine_wallet = '0xea674fdde714fd979de3edf0f56aa9716b898ec8'
big_random_miner = '0xdd619667be721974a21b22bf5e7d54e51adf9c01'
big_miner_2 ='0xddd31343c41ff761e674c5bfd74e043059fcb2d0'
old_miner = '0xdc82b8db4a2198443aa583c00ac54cba7b6d5039'
constant_decrease_miner = '0x72c013330cdfef5c4d8d5880944bc8cd953bd352'

def sum_ether_by_month(income_records: dict) -> list:
    """
        DEPRECATED__________________________DEPRECATED

        Get the total ether earned each month by this wallet from ethermine.org
        Deprecated

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
    :return: lsit of (date, ether earned that month)
    """
    months = Data_Cleaning.get_month_year_numbers()

    sum_monthly_income = {}
    for month_year in months:
        sum_monthly_income[month_year]=0.0 # initialize the dictionary

    with open('sum_ether_by_month_v2_log.txt','w') as log:
        for income_instance in income_records:
            income_month = income_instance[1][:7]
            # there is a problem with leading 0s on the month.
            # by removing leading zeros
            if income_month[5] == '0':
                start = income_month[:5]
                end = income_month[6:]
                income_month = start+end # reassigned leading zeros problem
            #print('you added {} to {}'.format(income_instance[0],income_month))
            try:
                sum_monthly_income[income_month] = sum_monthly_income[income_month] + income_instance[0]
            except:
                # this causes you to ignore the the data outside of the range you care about
                log.write('{} is outside side of the range Jan 2015 - Dec 2020'.format(str(income_instance)))

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


def get_wallet_income_from_ethermine(miner_address, get_date_of_first_income=True, simp=False):
    """
        This queires etherscan.io and stiches together the methods ot see the income and date of firstinceom
    :param miner_address: The wallet to Query
    :param get_date_of_first_income: boolean if you want the date for the first income
    :return: the list of tuples of month, income) and the date for first income
    """

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

    if simp:
        return sum_ether_by_month_v2(income_records)

    if get_date_of_first_income:
        try:
            date_of_first_income = datetime.datetime.strptime(income_records[0][1], '%Y-%m-%d %H:%M:%S')
        except:
            date_of_first_income = 'noIncome'

        try:
            monthly_income = sum_ether_by_month_v2(income_records) # form ("2016-3", 2.03252) : date, amount of ether.
        except:
            print(ethermine_wallet +' Broke it')

        return monthly_income, date_of_first_income
    else:
        return sum_ether_by_month_v2(income_records)


def read_in_wallet_addresses(filename ='ethermine_wallets_generated.csv'):
    """
        Get all of the wallets that have mined from ethermine.org this was created previously
        using the API_Methods.Commands_for_Ethermine_API.py

    :param filename: the location of where you are storing all the wallets that use ethermine.
    :return addresses: a list of wallets that mine at ethermine
    """
    with open (filename) as file_in:
        addresses = file_in.readlines()
        addresses =[a[:42] for a in addresses] # strip the carriage return
        return addresses

# this is too slow. I need a faster way of doing this.
def visualize_monthly_income(only_large_firms=False, simp=True):
    """
    See bar graphs of ether income from miners at ethermine.org
    :return: nothings just shows a graph
    """
    import time


    wallets = read_in_wallet_addresses()

    for wallet in wallets:

        monthly_income, date_of_first = get_wallet_income_from_ethermine(wallet,simp)

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


def generate_list_of_month_ids():
    """
        This write the months-Year in the form of 2020-6 to month_names.csv
        I moved this to utils.DataCleaning.get_month_year_numbers()
    """
    # Source: https://stackoverflow.com/questions/34898525/generate-list-of-months-between-interval-in-python
    all_months = pd.date_range('2015-1-1', '2020-12-31',
                  freq='MS').strftime("%Y-%b").tolist()

    with open("month_names.csv", 'w') as month_record:
        for m in all_months:
            year, mon = m.split('-')[0], m.split('-')[1]
            mon_as_num = strptime(mon,'%b').tm_mon # convert to months as number
            to_write = '{}-{}\n'.format(year,mon_as_num)
            month_record.write(to_write)


def create_relevant_miner_stats(miner_address):
    """
       Get the monthly  ether income data, wallet_address, and date of first income for a wallet.

    :param miner_address: the wallet to query

    :return:miner_record String: miner_address,date_first_income,str(monthly_income)
    """
    monthly_income, date_first_income = get_wallet_income_from_ethermine(miner_address,True)
    miner_record = '{},{},{}\n'.format(miner_address,date_first_income,str(monthly_income))
    return miner_record


def get_miner_stats_for_all_ethermine():
    """
        Walk through all of the wallets in ethermine_wallets_generated.csv
        create a new file and write out the payment details them
    """
    import time
    log = open('account_breaking_log.txt','a') # this tracks the wallets that break the API
    with open('miner_detailed_stats.csv','w') as out:
        out.write('wallet_address,date_of_first_income,array_of_monthly_ether_income\n')
        wallets = read_in_wallet_addresses()
        random.shuffle(wallets)
        counter =0
        for wallet in wallets:
            try:
                time.sleep(.2)
                counter+=1
                record = create_relevant_miner_stats(wallet)
                out.write(record)
                print('on {} of 90,000 wrote a record for {}'.format(counter,wallet))
            except:
                log.write(wallet + '\n')
                time.sleep(1) # this is to not overload the api

    log.close()


#get_miner_stats_for_all_ethermine()

visualize_monthly_income(simp=True)


# in theory this should never use more than 100MB of memory and ~%20 of ram

# I started this process and 1/15 at 1:48

#Right now I am getting about 120 calls a minute.
# pretty good should be able to do all of them in 12 hours. That is do able.

# you should just let this run all of tonight