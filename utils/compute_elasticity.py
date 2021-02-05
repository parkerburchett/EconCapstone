# this file compute the price elasticity of supply by miner.
# %change in derived GH/s / % change in usd value of GH/

import json
import add_zero_records_to_miners as add_zeros


"""
To get an elasticity score you need 4 months of data. You exclude every thing with 3 or less months of income. 

You want data saved in a large .csv file that looks like this:
miner_address, year_month(of start),
own-price elasticity between (year_month and year_month-1), 
Firm size (avg gh/s for the months considered),
Firm age (number of full months of income),
Dollar_value_of_ghs in year_month -2,
Dollar_value_of_ghs in year_month -3,
income from only Ethermine,
incoem from only SparkPool,
income from both Sparkpool and ethermine, 


"""



def get_all_months():
    """
    :return: A list of months in order where you could have data.
    """
    return ['2016-03', '2016-04', '2016-05', '2016-06', '2016-07', '2016-08', '2016-09', '2016-10', '2016-11', '2016-12',
            '2017-01', '2017-02', '2017-03', '2017-04', '2017-05', '2017-06', '2017-07', '2017-08', '2017-09', '2017-10',
            '2017-11', '2017-12', '2018-01', '2018-02', '2018-03', '2018-04', '2018-05', '2018-06', '2018-07', '2018-08',
            '2018-09', '2018-10', '2018-11', '2018-12', '2019-01', '2019-02', '2019-03', '2019-04', '2019-05', '2019-06',
            '2019-07', '2019-08', '2019-09', '2019-10', '2019-11', '2019-12', '2020-01', '2020-02', '2020-03', '2020-04',
            '2020-05', '2020-06', '2020-07', '2020-08', '2020-09', '2020-10', '2020-11', '2020-12']


def load_standard_form_json():
    """
        Read in the data from the json file. This is slower than just runnind add_zero_records_to_miners.main()

    :return: a dictionary of wallet: standard form income statements
    """
    with open (r'C:\Users\parke\Documents\GitHub\EconCapstone\datasets\ethermine_standard_form_data.json') as file_input:
        groups_in_standard_from = json.load(file_input)
        return groups_in_standard_from


def percent_change(current,previous):
    """
        Get the percent change  (rounded to 6 decimal places) between first and second.
        This can be negative or positive
        source: https://stackoverflow.com/questions/30926840/how-to-check-change-between-two-values-in-percent

    :param current: float
    :param previous: float
    :return: the % increase or decrase.
    """
    if current == previous:
        return 0
    try:
        return ((current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return float('inf')


def compute_GHs_elasticity(standard_form_group, months_with_data):
    """
        For the months that we have data (months_with_data) compute the % change in monthly GHs and price of GHs

            # I think the math here is wrong. I don't know why though.
            I am to tired to keep it in my head

        This ignores all zeros. I will need to add in the zeros later to fix it.

        maybe add in get months between (inclusive) start and end +1.

    :param standard_form_group:
    :return: (wallet, GH/s elasticity
    """

    wallet_address = standard_form_group[1][1]

    group_dict ={}
    for g in standard_form_group[1:]:
        group_dict[g[0]] = g # the year_month is the key

    derived_monthly_miner_ghs, derived_USD_value_of_ghs =[], []

    for month in months_with_data:
        derived_monthly_miner_ghs.append(float(group_dict[month][8]))
        derived_USD_value_of_ghs.append(float(group_dict[month][7]))
    elasticity_scores= []

    for i in range(len(months_with_data)-2): # untested
        cur_hashrate = derived_monthly_miner_ghs[i]
        next_hashrate =  derived_monthly_miner_ghs[i+1]
        change_hashrate = percent_change(next_hashrate,cur_hashrate)

        cur_price = derived_USD_value_of_ghs[i]
        next_price = derived_USD_value_of_ghs[i+1]
        change_price = percent_change(next_price, cur_price)

        elasticity = change_hashrate/change_price
        elasticity_scores.append(elasticity)

    return wallet_address, elasticity_scores


def get_months_to_consider(standard_form_group):
    """
            You only want the months between (exclusive) their first and last income.

    :param standard_form_group: A tuple of miner monthly income statements tuples
    :return: A list of months that will be used as keys to get the income statements you need.
    """
    all_months = get_all_months()

    first_month_with_income = None
    start_index = 0
    for i in range(1,len(standard_form_group)-1):
        if standard_form_group[i][2] != '0': # miner_monthly_income col
            print(standard_form_group[i])
            first_month_with_income = all_months[i]#2018-6
            start_index =i
            break

    end_index =59 # should be 58
    # walk backwards through standard_form_group
    for j in range(len(standard_form_group)-1,1,-1):
        if standard_form_group[j][2] != '0':  # miner_monthly_income
            last_month_with_data = all_months[j]
            end_index =j # correct
            break



    months_to_consider = all_months[start_index:end_index]
    return months_to_consider


def main():


    groups_in_standard_from_dict = add_zeros.get_sample_data_standard_from(5)
    wallets = list(groups_in_standard_from_dict.keys())

    for i in range(10):
        standard_form = groups_in_standard_from_dict[wallets[i]]
        months_to_consider = get_months_to_consider(standard_form)
        wallet, elasticity = compute_GHs_elasticity(standard_form,months_to_consider)


    print('fin')




main()











""""

for each miner

10 elasticity scores  = 


e1 = jan 2019 

e1 = PRICE(jan 2019-1) + more price data. 





"""