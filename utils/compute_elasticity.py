# this file compute the price elasticity of supply by miner.
# %change in derived GH/s / % change in usd value of GH/

import json
import add_zero_records_to_miners as add_zeros

def load_standard_form_json():
    """
        Read in the data from the json file

    :return: a dictionary of wallet: standard form income statements
    """
    with open (r'C:\Users\parke\Documents\GitHub\EconCapstone\datasets\ethermine_standard_form_data.json') as file_input:
        groups_in_standard_from = json.load(file_input)
        return groups_in_standard_from


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

    return elasticity_by_month

def determine_relevant_months(standard_form_group):
    """
        Get the list of months that this miner had income for

    :param standard_form_group: A group in standard from
    :return: a list of months where they have data

    """
    months_with_data = [statement[0] for statement in standard_form_group[1:] if statement[2] != '0']
    return months_with_data

def main():
    groups_in_standard_from_dict = add_zeros.get_sample_data_standard_from(5)
    wallets = list(groups_in_standard_from_dict.keys())

    for i in range(10):
        standard_form = groups_in_standard_from_dict[wallets[i]]
        months = determine_relevant_months(standard_form)
        wallet, elasticity = compute_GHs_elasticity(standard_form,months)


    print('fin')



main()