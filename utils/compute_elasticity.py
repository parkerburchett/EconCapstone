# this file compute the price elasticity of supply by miner.
# %change in derived GH/s / % change in usd value of GH/

import json
import add_zero_records_to_miners as add_zeros


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

    :param first: float
    :param second: float
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

            # I think the math here is wrong. I don't know why thouugh.
            I am to tired to keep it in my head

        This ignores all zeros. I will need to add in the zeros later to fix it.

        maybe add in get months between (inclusive) start and end +1.

    :param standard_form_group:
    :return: (wallet, GH/s elasticity
    """

    group_dict ={}
    for g in standard_form_group[1:]:
        group_dict[g[0]] = g

    derived_monthly_miner_ghs, derived_USD_value_of_ghs =[], []

    for month in months_with_data:
        derived_monthly_miner_ghs.append(float(group_dict[month][8]))
        derived_USD_value_of_ghs.append(float(group_dict[month][7]))
    elasticity_by_month = []
    for i in range(len(months_with_data)-2):
        cur_hashrate = derived_monthly_miner_ghs[i]
        next_hashrate =  derived_monthly_miner_ghs[i+1]
        average_hashrate = (cur_hashrate + next_hashrate) /2

        cur_price = derived_USD_value_of_ghs[i]
        next_price = derived_USD_value_of_ghs[i+1]
        average_price = (cur_price + next_price)/2

        elasticity = ((next_hashrate - cur_hashrate)/average_hashrate) / ((next_price - cur_price)/average_price)
        elasticity_by_month.append((month,elasticity))
    import numpy as np
    average_elasticity = np.average(x[1] for x in elasticity_by_month)
    return elasticity_by_month


def get_months_to_consider(standard_form_group, trailing_zeros=1):
    """
            NOTE: this is not rigeriously tested. There are some edge cases that might break this.
            such as when the range is from 0-58 or the entire range.

            Returns the months to consider for each miner. That = Every month from the starting month + a month for each trailing zero
    :param standard_form_group: A tuple of miner monthly income statements tuples
    :param trailing_zeros: the number of months with no income, after the last month, to consider.
    :return: A list of months that will be used as keys to get the income statements you need.
    """
    all_months = get_all_months()

    first_month_with_income = None
    start_index = 0
    for i in range(1,len(standard_form_group)-1):
        if standard_form_group[i][2] != '0': # miner_monthly_income col
            print(standard_form_group[i])
            first_month_with_income = all_months[i-1]#2018-6
            start_index =i-1
            break

    end_index =59 # should be 58
    # walk backwards through standard_form_group
    for j in range(len(standard_form_group)-1,1,-1):
        if standard_form_group[j][2] != '0':  # miner_monthly_income
            last_month_with_data = all_months[j]
            end_index =j # correct
            break

    if end_index != 58: # 59 might be wrong
        num_months = end_index -start_index
    else:
        num_months = 59 - start_index + trailing_zeros # untested

    months_to_consider = all_months[start_index:end_index+1+trailing_zeros]

    return months_to_consider


def main():
    groups_in_standard_from_dict = add_zeros.get_sample_data_standard_from(5)
    wallets = list(groups_in_standard_from_dict.keys())

    for i in range(10):
        standard_form = groups_in_standard_from_dict[wallets[i]]
        months = get_months_to_consider(standard_form)
        wallet, elasticity = compute_GHs_elasticity(standard_form,months)


    print('fin')




main()