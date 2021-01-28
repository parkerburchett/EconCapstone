# In order to get an accurate change in monthly reveune, the months that have no income need have 0s manaully added.

# This program takes in two files
# datasets/default_miner_data.csv : the template for all of the zeros.


# I am choosing to exclude all 2021-01 and stuff that only has a single


# It makes more sense to walk through them in chunks.
# There is a problem where the income statements are broken up accross two files


import os
import csv
import glob
import numpy as np
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



def merge_miner_groups(groups_A, groups_B):
    """
        This solves having miner data split accross the two files.

    :param groups_A: a miner_group generated from file i
    :param groups_B: a miner_group generated from file i+1
    :return:  first, second miner_groups
    """
    A_n = groups_A.pop(-1)
    A_n_miner = A_n[1]

    if isinstance(A_n[0], str):
        A_n = [A_n]  # cast as a list of lists

    A_n_less_1 = groups_A.pop(-1)
    A_n_less_1_miner = A_n_less_1[0][1]

    B_0 = groups_B.pop(0)
    B_0_miner = B_0[0][1]

    merge_first = False
    merge_second = False

    if A_n_miner == A_n_less_1_miner: # should be ==
        # merge these two since they have the same miner
        A_n_less_1.append(A_n)
        merge_first = True

    if A_n_miner == B_0_miner:
        if merge_first:
            merge_second = True
            for record in B_0:
                A_n_less_1.append(record)
        else:
            merge_second = True
            for record in B_0:
                A_n.append(record)


    if merge_first and merge_second:
        # in this case A_n, A_n_less_1 and B_0 all refer to the same miner.
        # print('all refer to the same miner')
        # print('that miner is {}'.format(A_n_miner))
        groups_A.append(A_n_less_1)

    elif merge_first and not merge_second:
        # you have two miners A_n_less_1 and B_0
        # print('you have two miners A_n_less_1 and B_0')
        # print('Those miners are the last in first {} and the first in the second {}'.format(A_n_less_1_miner,B_0_miner))
        groups_A.append(A_n_less_1)
        groups_A.append(B_0)

    elif not merge_first and merge_second:
        # you have two miners, stored in A_n_less_1 and A_n
        # print('you have two miners, stored in A_n_less_1 and A_n')
        # print('Those miners are the last in second to last in A {} and the first in the second {}'.format(A_n_less_1_miner, A_n_miner))
        groups_A.append(A_n_less_1)
        groups_A.append(A_n)

    else:
        # you have three unique miners
        # case for files 001 and 002.
        # print('you have three unique miners.')
        # print('Miners in alphabetical order are \n{}\n{}\n{}'.format(A_n_less_1_miner,A_n_miner,B_0_miner))
        groups_A.append(A_n_less_1)
        groups_A.append(A_n)
        groups_A.append(B_0)


    return groups_A, groups_B


def main():
    """
        This stiches together all of the methods to group miners into list of list of their own income statements.
        # this is slightly inefficient, since it reads every file twice.
        I need to rewrite that to fix it.
        # right now it only takes about 5 minutes to run
    :return:
    """
    default = build_default_miner_revenue()
    second =[]
    file_names = get_csv_part_file_names()
    count_unique_miners = 0
    for i in range(199):
        print("merging files {} and {}".format(i, i+1))
        miner_data1 = load_single_file(file_names[i])
        first = group_miner_income(miner_data1)
        miner_data2 = load_single_file(file_names[i+1])
        second = group_miner_income(miner_data2)
        first, second = merge_miner_groups(first, second)
        count_unique_miners += len(first)

        print(count_unique_miners)

    num_miners_in_second = len(second)
    print('In this program there are {} unique miners'.format(num_miners_in_second + count_unique_miners))
    print("there should be approx exactly 593674 miners with data")
    print('you are missing {} off from the correct solution'.format(num_miners_in_second + count_unique_miners - 593674 ))









main()