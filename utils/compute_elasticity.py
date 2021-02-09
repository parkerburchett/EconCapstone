# this file compute the price elasticity of supply by miner.
# %change in derived GH/s / % change in usd value of GH/

import json
import numpy as np
import csv
import copy # unclear fi you need to deep copy the values.
import add_zero_records_to_miners as add_zeros

outline="""
To get an elasticity score you need 4 months of data. You exclude every thing with 3 or less months of income. 

You want data saved in a large .csv file that looks like this:
miner_address, year_month(of start),
own-price elasticity between (year_month and year_month-1), 
Firm size (avg gh/s for the months considered),
Firm age (number of full months of income),
Dollar_value_of_ghs in year_month -2, this is price at t-2
Dollar_value_of_ghs in year_month -3, this is price at t-3 
source:ethermine

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

# unused
def load_standard_form_json():
    """
        Read in the data from the json file. This is slower than just runnind add_zero_records_to_miners.main()

    :return: a dictionary of wallet: standard form income statements
    """
    with open (r'C:\Users\parke\Documents\GitHub\EconCapstone\datasets\ethermine_standard_form_data.json') as file_input:
        groups_in_standard_from = json.load(file_input)
        return groups_in_standard_from


#OLD
def get_months_to_consider(standard_form_group):
    """
            You only want the months between (exclusive) their first and last income.

    :param standard_form_group: A tuple of miner monthly income statements tuples
    :return: A list of months that will be used as keys to get the income statements you need.
    """
    all_months = get_all_months()
    months_with_income = 0
    for i in range(1,len(standard_form_group)-1):
        if standard_form_group[i][2] != '0':
            months_with_income+=1

    first_month_with_income = None
    start_index = 0
    for i in range(1,len(standard_form_group)-1):
        if standard_form_group[i][2] != '0': # miner_monthly_income col
            first_month_with_income = all_months[i] #2018-6
            start_index =i
            break

    end_index =59 # should be 58
    # walk backwards through standard_form_group
    for j in range(len(standard_form_group)-2,1,-1):
        if standard_form_group[j][2] != '0':  # miner_monthly_income
            last_month_with_data = all_months[j]
            end_index =j # correct
            break
    months_to_consider = all_months[start_index+1:end_index-1]
    return months_to_consider


# old
def compute_GHs_elasticity(standard_form_group, full_months):
    """
        For the months that we have data (full_months) compute the % change in monthly GHs and price of GHs

    :param standard_form_group:
    :param full_months: a list of months you are treating as data.

    :return: elasticity_dict : a dictionary where the key is the year_month and the value is the elastity score for that
            month and teh previous. or Unknown otherwise.
    """
    if len(full_months) < 4:
        res = input('this wallet was bad 3 or less months with data. press any key to continue')
        return

    elif len(full_months) == 4:
        # you only get a single elasticy for the 3rd element.
        group_dict = {}
        for g in standard_form_group[1:]:
            group_dict[g[0]] = g  # the year_month is the key

        derived_monthly_miner_ghs = []
        derived_USD_value_of_ghs =  []

        for month in full_months:
            derived_monthly_miner_ghs.append(float(group_dict[month][8]))
            derived_USD_value_of_ghs.append(float(group_dict[month][7]))

        elasticity_dict = {}  # key is month_year: elasticity for that month with prev month.
        cur_hashrate = derived_monthly_miner_ghs[2]
        prev_hashrate = derived_monthly_miner_ghs[2 - 1]
        change_hashrate = percent_change(current=cur_hashrate, previous=prev_hashrate)

        cur_price = derived_USD_value_of_ghs[2]
        prev_price = derived_USD_value_of_ghs[2 - 1]
        change_price = percent_change(current=cur_price, previous=prev_price)

        elasticity = change_hashrate / change_price
        month = full_months[2] # the third month is the only elasticity scores that matter
        elasticity_dict[month] = elasticity

        elasticity_dict[full_months[1]] ='Unknownn'

    else:
        # normal case: len>=5.
        group_dict ={}
        for g in standard_form_group[1:]:
            group_dict[g[0]] = g # the year_month is the key

        derived_monthly_miner_ghs = []
        derived_USD_value_of_ghs  = []

        for month in full_months:
            derived_monthly_miner_ghs.append(float(group_dict[month][8]))
            derived_USD_value_of_ghs.append(float(group_dict[month][7]))

        elasticity_dict ={} # key is month_year: elasticity for that month with prev month.

        ## If you only have 4 montsh, 1,2,3,4 you will only get an elastiticy for between month 2,3 THis is stored in month 3

        last_index = len(full_months) - 1
        for i in range(1, last_index): # untested
            cur_hashrate = derived_monthly_miner_ghs[i]
            prev_hashrate =  derived_monthly_miner_ghs[i-1]
            change_hashrate = percent_change(current=cur_hashrate,previous=prev_hashrate)

            cur_price = derived_USD_value_of_ghs[i]
            prev_price = derived_USD_value_of_ghs[i-1]
            change_price = percent_change(current=cur_price,previous=prev_price)

            elasticity = change_hashrate/change_price

            month = full_months[i]
            elasticity_dict[month] = elasticity # assign the elasticity score to the proper month.
            elasticity_dict[full_months[0]] = 'Unknown'
    return elasticity_dict

# old bad
def get_final_data(group, months_to_consider):
    """
    Get the array of the final data
    miner_address,
    year_month(of start),
    own-price elasticity between (year_month and year_month-1),
    Firm size (avg gh/s for the months considered),
    Firm age (number of full months of income),
    Dollar_value_of_ghs in year_month -2,
    Dollar_value_of_ghs in year_month -3,
    :param months_to_consider: The months with data.
    :param group: a tuple of tuples.

    :return:
    """
    if len(months_to_consider) ==0:
        return 'no records'

    group_dict = {} #cast it as a dict with the key being the previous month
    for g in group[1:]:
        group_dict[g[0]] = g

    first_month = months_to_consider[0]
    all_months = get_all_months()
    wallet_address = group[1][1]

    ## elasticity_dict is a single month off. it says 2018-08 is unknown when 2018-2018 shoul should a score since it is the second full month.
    elasticity_dict = compute_GHs_elasticity(standard_form_group=group, full_months=months_to_consider) # untested
    firm_size =  get_firm_size(group_dict,months_to_consider)
    firm_age, firm_start = get_firm_age(group_dict, months_to_consider)
    records_to_return = []
    # key might be bad
    for month in months_to_consider[1:-1]:
        month_index = all_months.index(month)
        prev_month = all_months[month_index-1]
        prev_prev_month = all_months[month_index-2]
        prev_prev_prev_month =all_months[month_index-3]

        cur_month_elasticity = elasticity_dict[month]

        month_record = (wallet_address,
                        'Ethermine',
                        firm_start,
                        firm_size,
                        firm_age,
                        month,
                        cur_month_elasticity,
                        float(group_dict[prev_prev_month][7]), # t-2
                        float(group_dict[prev_prev_prev_month][7])# t-3
                        )

        records_to_return.append(month_record)

    return records_to_return

################# utils #################

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


def get_previous_month(month):
    """
        Return as a string the previous month

    :param month:
    :return: The previous month to this month
    """
    all_months =  get_all_months()
    i  = all_months.index(month)
    try:
        return all_months[i-1]
    except:
        return all_months[i]


def has_income(month_entry):
    """

        Return True it this month has ETH income,
        Else Return false
        A row inside of standard_form_group
    """
    return month_entry[2] != '0'


def get_months_between_inclusive(start_month, end_month):
    """
        Get a list of the months between start_month and end month. inclusive

    :param start_month:
    :param end_month:
    :return:
    """
    all_months =get_all_months()
    start_index = all_months.index(start_month)
    end_index = all_months.index(end_month)
    months_between = all_months[start_index:end_index+1]
    return months_between


def get_firm_size(group_dict, months_with_elasticity):
    """
        Size is average Derived GH/s.
    :param group:
    :param months_to_consider:
    :return:
    """

    for month in months_with_elasticity:
        all_income_statements = float(group_dict[month][2])

    return np.average(all_income_statements) # untested


def get_firm_age(full_months):
    """
        Age is Number of months with income, and month of first full income
    :param group_dict:
    :param months_to_consider:
    :return: Number of full months with income, date of month with first full income.
        Number of full months with income, income of first month
    """
    return len(full_months), full_months[0]


def cast_standard_form_group_as_dict(group_standard_from):
    group_dict = {}  # cast it as a dict with the key being the previous month
    for g in group_standard_from[1:]:
        group_dict[g[0]] = g
    return group_dict


def create_ghs_value_dict(group_dict):
    ghs_value_dict = {}
    months = group_dict.keys()
    for month in months:
        ghs_value_dict[month] = float(group_dict[month][7]) # not sure if right index
    return ghs_value_dict


def create_miner_ghs_dict(group_dict):
    miner_ghs_dict = {}
    months = list(group_dict.keys())
    for month in months:
        miner_ghs_dict[month] = float(group_dict[month][8]) # not sure if right index
    return miner_ghs_dict


def get_elasticity_for_month(month, ghs_value_dict, miner_ghs_dict):
    """
        Get the GH/s elasticity score for this month based on a Standard_form_dict for this month.
        You pass this a list of months with elasticity

    :param month: the month you are computing the elasticity between this and the previous month
    :param standard_form_dict:
    :return: A float representing the GH/s price elasticity score for this month.
    """
    prev_month = get_previous_month(month)

    cur_hashrate = miner_ghs_dict[month]
    prev_hashrate = miner_ghs_dict[prev_month]
    change_hashrate = percent_change(current=cur_hashrate, previous=prev_hashrate)

    cur_GHS_value = ghs_value_dict[month]
    prev_GHS_value = ghs_value_dict[prev_month]
    change_GHS_value = percent_change(current=cur_GHS_value, previous=prev_GHS_value)

    elasticity = change_hashrate / change_GHS_value
    return elasticity


def get_full_months(standard_form_group):
    """
        Returns a list of months will full entire month income

    :param standard_form_group:
    :return: A list of months that will have an entire month of income
    """
    months_with_income = []
    for row in standard_form_group[1:]:
        if has_income(row):
            months_with_income.append(row[0])
    if len(months_with_income) == 0:
        return []

    first_month = months_with_income[0]
    last_month = months_with_income[-1]

    months_between_first_and_last = get_months_between_inclusive(first_month,last_month)
    if len(months_between_first_and_last) <=2:
        return []
    else:
        full_months = months_between_first_and_last[1:-1] # strip the first and last since they could be partial months.
        return full_months


################# utils #################

def refactored_get_final_row(standard_form_group):
    """
        Pass this a standard_form_group an d it will return a list of the final rows to write to the file

    :param standard_form_group:
    :return: results[] array of array in the form
    'wallet_address, pool_name, firm_first_full_month, firm_size, firm_age, month, GHs_elasticity, prev_month_GHs_value, prev_prev_month_GHs_value'
    """
    group_dict = cast_standard_form_group_as_dict(standard_form_group)
    full_months = get_full_months(standard_form_group)
    wallet_address = group_dict['2020-10'][1] # just the wallet address, all are the same you can pick any month
    months_with_elasticity = full_months[1:-1]  # should be two month less.
    if len(months_with_elasticity) == 0:
        return []
    ghs_value_dict = create_ghs_value_dict(group_dict)
    miner_ghs_dict = create_miner_ghs_dict(group_dict)
    firm_size = get_firm_size(group_dict, full_months)
    firm_age, firm_start = get_firm_age(full_months)
    pool_name= 'Ethermine'
    results=[]
    for month in months_with_elasticity:
        cur_elasticity = get_elasticity_for_month(month, ghs_value_dict, miner_ghs_dict)
        prev2_month = get_previous_month(month)
        prev3_month = get_previous_month(prev2_month)
        a_row = (wallet_address,
                 pool_name,
                 firm_start,
                 firm_size,
                 firm_age,
                 month,
                 cur_elasticity,
                 ghs_value_dict[prev2_month],
                 ghs_value_dict[prev3_month])
        results.append(copy.deepcopy(a_row))

    return results




def main():


    groups_in_standard_from_dict = add_zeros.get_data_into_standard_form()
    wallets = list(groups_in_standard_from_dict.keys())
    with open(r'C:\Users\parke\Documents\GitHub\EconCapstone\utils\final_data_out.csv','w', newline='', encoding='utf-8') as out:
        out.write('wallet_address, pool_name, firm_first_full_month, firm_size, firm_age, month, GHs_elasticity, prev_month_GHs_value, prev_prev_month_GHs_value\n')
        writer = csv.writer(out)
        a =0
        for wallet in wallets:
            standard_form_group = groups_in_standard_from_dict[wallet]
            records_for_wallet_i = refactored_get_final_row(standard_form_group)
            writer.writerows(records_for_wallet_i)
            a+=1
            if a % 10000 == 0:
                print('wrote {} wallets'.format(a))






    print('fin')




main()











""""

for each miner

10 elasticity scores  = 


e1 = jan 2019 

e1 = PRICE(jan 2019-1) + more price data. 





"""