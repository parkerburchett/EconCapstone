# In order to get an accurate change in monthly reveune, the months that have no income need have 0s manaully added.

# This program takes in two files
# datasets/default_miner_data.csv : the template for all of the zeros.
# I am choosing to exclude all 2021-01 because I don't have a full month for it.


import os
import csv
import glob
import json
import matplotlib.pyplot as plt


def get_raw_data_file_names():
    os.chdir(r'C:\Users\parke\Documents\GitHub\EconCapstone\datasets\csv_miner_data_parts')
    all_filenames = [i for i in glob.glob('*.csv')]
    return all_filenames


def get_column_names():
    return ['year_month',
          'to_address',
          'miner_monthly_eth_revenue',
          'average_eth_market_price',
          'global_average_hashrate',
          'monthly_new_eth',
          'derived_ghs_required_for_one_eth',
          'derived_USD_value_of_ghs',
          'derived_monthly_miner_ghs',
          'derived_miner_monthly_USD_revenue']


def load_single_file(filename):
    with open(filename,'r') as input:
        reader = csv.reader(input)
        lines = [row for row in reader]
        return lines


def build_default_miner_template():
    with open(r'C:\Users\parke\Documents\GitHub\EconCapstone\datasets\default_miner_data.csv', 'r') as default:
        reader = csv.reader(default)
        default_lines = [line for line in reader]
        return default_lines


def partition_complete_uncomplete_income_statements(miner_data):
    """
        This takes in a list of miner_income statements and returns two lists.
            A list of income statements that is complete and one that is maybe complete.

    :param miner_data: A list fo miner income from load_single_file :return: complete_income_statements: a list of
    :return:
    income statements. If a miner in in here, all of the miner's income statements are there.
    possibly_complete_income_statements : a list of miner income statements whose addresses are the first or last in

    """
    first_miner_address = miner_data[0][1]
    last_miner_address = miner_data[-1][1]
    complete_income_statements = []
    possibly_complete_income_statements = []

    for statement in miner_data:
        if statement[1] == first_miner_address or statement[1] == last_miner_address:
            # if the income statement is for the first or last miner
            possibly_complete_income_statements.append(statement)
        else:
            complete_income_statements.append(statement)

    return complete_income_statements, possibly_complete_income_statements


def group_miner_income_statements(complete_miner_income):
    """
        Pass this a list of income statements. It returns those income statements packaged into sublists one for each miner
    :param complete_miner_income: generate_complete_and_unknown_complete_miner_groups. A list of income statements for the miner.
    :return: The data grouped in to a list of lists where each element in teh first list is all the miner data I have for them
    """
    groups = []
    start = 0
    last_miner_address = complete_miner_income[-1][1]
    for i in range(len(complete_miner_income)-1):
        if complete_miner_income[start][1] != complete_miner_income[i][1]:
            full_miner = complete_miner_income[start:i]
            groups.append(full_miner)
            start = i

    last_group = []
    for i in range(len(complete_miner_income)-1):
        if complete_miner_income[i][1] == last_miner_address:
            last_group.append(complete_miner_income[i])
    groups.append(last_group)
    return groups


def group_miners_from_files(file_names):
    """
        Read each file in file_names and group the miner income statements into lists that only consider a single miner

    :param file_names: the names of the files with the raw data
    :return: grouped_miner_statements: A list of lists. Each sublist is all of the income statements for a miner.
    """

    #file_names = get_raw_data_file_names()
    left_over_statements = []
    grouped_miner_statements = []
    counter = 0
    for file in file_names:
        complete, possibly_complete = partition_complete_uncomplete_income_statements(load_single_file(file))
        complete_groups = group_miner_income_statements(complete)
        left_over_statements.extend(possibly_complete)
        grouped_miner_statements.extend(complete_groups)
        counter += 1
        print('Grouped a file {} with {} addresses'.format(counter,len(complete_groups)))

    # sort left_over_statements
    left_over_statements.sort(key=lambda x: x[1]) # sort by wallet.
    left_over_groups = group_miner_income_statements(left_over_statements)

    print('There are {} left overs'.format(len(left_over_groups)))
    print('Before you add in the leftovers you are down {} records'.format(593674 - len(grouped_miner_statements)))
    grouped_miner_statements.extend(left_over_groups)
    print("there should be exactly 593674 miners with data")
    print('you are missing {} off from the correct number of wallets. I dont know why those are lost'.format(593674 - len(grouped_miner_statements)))
    # I lost 52 records from when I downloaded them from jupyter notebooks. I can't find where I lost those
    return grouped_miner_statements


def cast_income_group_as_standard_form(group,default):
    """
        You need to add zeros to properly look at the correlation between implied gh/s and

    :param group: A list of all the monthly income statements I have for a particular miner.
    :param default: A list of all the constants that you care about.
    :return: standard_form: the data now in standard form where the data is
    """
    # cast group as a dictionary where the key is the month_year.

    dict_of_group ={}

    if len(group)==0:
        return

    for g in group:
        dict_of_group[g[0]] = g # key is year_month:  value is the data for that month. Including the month_year

    wallet_address = group[0][1]
    standard_form =[(default[0])]
    months_with_data = [x[0] for x in group]

    for s in default[1:]: # ignore the first row since it is the header
        if s[0] in months_with_data:
            s = dict_of_group[s[0]]
        s[1] = wallet_address
        standard_form.append(tuple(s))

    standard_form =  tuple(standard_form)
    return standard_form


def show_histogram_of_firm_age(all_groups):
    """
    Create a histogram in matplotlib of number of months of income each firm has.
    Interestingly this shows a very steep drop off for each month. About 35% of all my miners
    only have a single month of income.
    :param all_groups: a group for every miner with an income statement
    :return: a matplotlib histogram of firm age.
    """
    num_months_with_income = [len(x) for x in all_groups]
    plt.hist(num_months_with_income, bins=[x for x in range(60)])
    plt.show()


def convert_groups_to_standard_form(all_groups):
    """
        Convert all income groups in to a list of miners where their monthly income is in standard form.

    :param all_groups: A list of lists. Each element is every monthly income statement for that miner.
    :return: all_standard_form: all of the miners where, for the months they have no income, there is a 0 in the monthly income
    """
    default = build_default_miner_template()
    all_standard_form = []
    counter = 0
    for group in all_groups:
        standard_form = cast_income_group_as_standard_form(group,default)
        all_standard_form.append(standard_form)
        counter+=1
        if counter % 10000 == 0:
            print('casted {} miners into the default'.format(counter))
            # this is just to visualize progress.

    return all_standard_form


def convert_standard_form_to_dict(groups_in_standard_form):
    """
        Create a dictionary object where the key is the wallet and the value it the standard from of that wallet

    :param groups_in_standard_form: A list of miner groups in standard form. Standard form is where all of the months
    are considered and 0 exist where a miner had no income.
    :return:all_groups_as_dict: the key is the wallet, the values are the standard form income statements of that wallet.
    """
    all_groups_as_dict = {}
    c =0
    for group in groups_in_standard_form:
        c +=1
        if type(group) is tuple:
            wallet_address = group[1][1]
            all_groups_as_dict[wallet_address] = group
        if c % 10000 ==0:
             print('{} cast as dicts'.format(c))
    return all_groups_as_dict


def write_dict_to_json(all_groups_as_dict):
    """
        Save the standard form as a json.

    :param all_groups_as_dict: A dictionary object where the key is the wallet address and the value are
    the standard form income statements of that wallet
    :return: nothing
    """
    try:
        out = open(r'C:\Users\parke\Documents\GitHub\EconCapstone\datasets\ethermine_standard_form_data.json','x')
    except:
        out = open(r'C:\Users\parke\Documents\GitHub\EconCapstone\datasets\ethermine_standard_form_data.json', 'w')
    out.seek(0)# this makes it overwrite the existing file

    json.dump(all_groups_as_dict,out)

    # this takes 5ish  minutes to dump the entire data in standard form.
    # the ethermine data is then 4.5G.
    out.close()

def get_sample_data_standard_from(size=10):
    file_names = get_raw_data_file_names()
    all_groups = group_miners_from_files(file_names[:size])
    groups_in_standard_form = convert_groups_to_standard_form(all_groups)
    all_groups_as_dict = convert_standard_form_to_dict(groups_in_standard_form)
    return all_groups_as_dict

def get_data_into_standard_form():
    file_names = get_raw_data_file_names()
    all_groups = group_miners_from_files(file_names)
    groups_in_standard_form = convert_groups_to_standard_form(all_groups)
    all_groups_as_dict =  convert_standard_form_to_dict(groups_in_standard_form)
    return all_groups_as_dict