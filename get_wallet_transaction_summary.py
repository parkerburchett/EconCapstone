from API_Methods import Etherscan_API
import matplotlib.pyplot as plt
import datetime
import random



ethermine_wallet = '0xea674fdde714fd979de3edf0f56aa9716b898ec8'
big_random_miner = '0xdd619667be721974a21b22bf5e7d54e51adf9c01'
big_miner_2 ='0xddd31343c41ff761e674c5bfd74e043059fcb2d0'
old_miner = '0xdc82b8db4a2198443aa583c00ac54cba7b6d5039'
constant_decrease_miner = '0x72c013330cdfef5c4d8d5880944bc8cd953bd352'

def sum_ether_by_month(income_records: dict) -> list:
    """
        Get the total ether earned each month by this wallet from ethermine.
    Source:
    # https://stackoverflow.com/questions/43235416/group-tuple-according-to-date-in-python
    :rtype: list
    :param income_records: A list of tuples of (datetime, income in ether from ethermien)
    :return: dict of (date: ether earned that month) for every month that there is income
    """
    months = list(set(['-'.join(item[1].split('-')[:2]) for item in income_records]))

    grouped_data = [[x[0] for x in income_records if '-'.join(x[1].split('-')[:2]) == month] for month in months]

    summation_as_dict = {month: sum(item) for month, item in zip(months, grouped_data)}

    summation_as_list = list(summation_as_dict.items())

    summation_as_list.sort(key=lambda x: x[0]) # sort by month
    return summation_as_list

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
    plt.xlabel('Month ')
    plt.ylabel('Ether')
    plt.xticks(rotation=45)

    plt.title('Ether Per Month Since Start')

    plt.show()



# you need a method that overlays the %change in income with the % change in average monthly price
# also with the previous month high.
# also with the previous-1 month high.

def get_wallet_income_from_ethermine(miner_address):
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

    date_of_first_income = datetime.datetime.strptime(income_records[0][1], '%Y-%m-%d %H:%M:%S')
    monthly_income = sum_ether_by_month(income_records)

        # you need to find a way to make all of the income statements map onto the same dictionary. in the last 6 years
    return monthly_income

def read_in_wallet_addresses(filename ='ethermine_wallets_generated.csv'):
    """

    :param filename: the location of where you are storing all the wallets that use ethermine.
    :return addreseses: a list of wallets that mine at ethermine
    """

    with open (filename) as file_in:
        addresses = file_in.readlines()
        addresses =[a[:42] for a in addresses] # strip the carriage return
        random.shuffle(addresses)
        return addresses


def visualize_monthly_income(only_large_firms=False):
    """
    See bar graphs of ether income from miners at ethermine.org
    :return:
    """
    wallets = read_in_wallet_addresses()
    for wallet in wallets:
        monthly_income = get_wallet_income_from_ethermine(wallet)

        if not only_large_firms:
            create_bar_plot_income(monthly_income)
        else:
            # this is a simple way to see if it is large
            # there is no reason to choose this standard over anther one
            total_income = [income[1] for income in monthly_income[:10]]
            if sum(total_income)>100: # if in the first 10 incomes sum to more than a 100 ethers
                print('{} is a large firm'.format(wallet))
                create_bar_plot_income(monthly_income)

visualize_monthly_income(only_large_firms=True)