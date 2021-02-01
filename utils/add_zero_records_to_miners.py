# In order to get an accurate change in monthly reveune, the months that have no income need have 0s manaully added.

# This program takes in two files
# datasets/default_miner_data.csv : the template for all of the zeros.
# I am choosing to exclude all 2021-01 because I don't have a full month for it.


import os
import csv
import glob
import copy


def get_csv_part_file_names():
    os.chdir(r'C:\Users\parke\Documents\GitHub\EconCapstone\datasets\csv_miner_data_parts')
    all_filenames = [i for i in glob.glob('*.csv')]
    return all_filenames


def get_header():
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


def build_default_miner_revenue():
    with open(r'C:\Users\parke\Documents\GitHub\EconCapstone\datasets\default_miner_data.csv', 'r') as default:
        reader = csv.reader(default)
        default_lines  = [line for line in reader]
        return default_lines


def group_miner_income(miner_data):
    """
        # Take miner_data and group it by wallet address
        This returns a list of lists of miner_monthly incomes where each list is all of the income statements of that miner.

    :param miner_income_statements: a list of arrays of every miner.
    :return: a array of single_miners where all of those income statements come from a single miner. Where each tuple stores all the the income statements for a particular miner.
    """
    miner_grouped_list = []
    single_miner = []
    while len(miner_data) > 1:
        if len(single_miner) == 0 and miner_data[0][1] != miner_data[1][1]:
            single_miner = miner_data.pop(0)
            copy_of_single_miner = copy.deepcopy(single_miner)
            single_miner = []
            miner_grouped_list.append([copy_of_single_miner])

        elif miner_data[0][1] == miner_data[1][1]:
            cur_line = miner_data.pop(0)
            single_miner.append(cur_line) # might need to be .extend

        else: # the miners are different
            cur_line = miner_data.pop(0)
            single_miner.append(cur_line)
            copy_of_single_miner = copy.deepcopy(single_miner)
            single_miner =[]
            miner_grouped_list.append(copy_of_single_miner)

    miner_grouped_list.append(miner_data.pop(0))
    return miner_grouped_list

    # at this point miner_data[0][1] is the last mining address in that file.
    # one of a 3 things must be true
    # for 001 the last miner is *359e
    # 1 this is the only mining income. eg in the next file. the first miner is different.]


def generate_complete_and_unknown_complete_miner_groups(miner_data):
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
            possibly_complete_income_statements.append(statement)
        else:
            complete_income_statements.append(statement)

    return complete_income_statements, possibly_complete_income_statements


def group_miner_income_statements(complete_miner_income):
    """
        Pass this a list of income statements, It returns those income statements packaged into lists when
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

def fully_group_miner_data():
    """

    :return: grouped_miner_statements: a list of lists of miner_income statements.
    Each element is all of the income statements I have for that miner.
    """
    
    file_names = get_csv_part_file_names()
    left_over_statements = []
    grouped_miner_statements = []
    counter =0
    for file in file_names:
        complete, possibly_complete = generate_complete_and_unknown_complete_miner_groups(load_single_file(file))
        complete_groups = group_miner_income_statements(complete)
        left_over_statements.extend(possibly_complete)
        grouped_miner_statements.extend(complete_groups)
        counter +=1
        print('Grouped a file {} with {} addresses'.format(counter,len(complete_groups)))


    # sort left_over_statements
    left_over_statements.sort(key=lambda x: x[1])
    left_over_groups = group_miner_income_statements(left_over_statements)

    print(' there are {} left overs'.format(len(left_over_groups)))
    print('before you add in the leftovers you are down {} records'.format(593674 - len(grouped_miner_statements)))
    grouped_miner_statements.extend(left_over_groups)
    print("there should be exactly 593674 miners with data")
    print('you are missing {} off from the correct solution. I dont know why those are lost'.format(593674 - len(grouped_miner_statements)))
    # I lost 52 records from when I downloaded them from jypter notebooks. I Can't find where I lost those

    return grouped_miner_statements

fully_group_miner_data()