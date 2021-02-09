import pandas as pd

def main():
    df = pd.read_csv(r"C:\Users\parke\Documents\GitHub\EconCapstone\utils\clean_final_data_out.csv")


    relevant_cols = [' firm_size',' firm_age', ' eth_earned_this_month', ' GHs_elasticity',]


    print(df[' GHs_elasticity'].describe())
    print(df[' GHs_elasticity'].median())

    for name in relevant_cols:
        average = round(df[name].mean(),4)
        std_dev = round(df[name].std(),4)
        print('Name: {} Average :{} std_dv: {}'.format(name,average,std_dev))


main()