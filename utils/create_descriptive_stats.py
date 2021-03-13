import pandas as pd

def main():
    df = pd.read_csv(r"C:\Users\parke\Documents\GitHub\EconCapstone\utils\CleanFinalDataNoOutliers.csv")
    print(df.columns)

    relevant_cols = [' firm_size',' firm_age', ' eth_earned_this_month', ' GHs_elasticity',' prev_month_GHs_value']

    print('DESCRIPTIVE STATS ON GH/S ELASTICITY')
    print(df[' GHs_elasticity'].describe(percentiles=[.01,.05,.1,.2,.3,.4,.5,.6,.7,.8,.9,.95,.99]).apply(lambda x: format(x, 'f')))
    print('median', df[' GHs_elasticity'].median())

    for name in relevant_cols:
        average = round(df[name].mean(),6)
        std_dev = round(df[name].std(),6)
        count = df[name].count()
        print('Name: {} Average :{} Count {}std_dev: {}'.format(name,average,count,std_dev))


def get_unique_miner_descriptive_stats():
    """
        Compute the average and following values for Firm Age and Firm size. 
        
        In the paper you submit to journals you want to use average GH/s instead of average ETH.

        The new dependent variables out to be the GH/s instead of the elasticity. 



    """

    df = pd.read_csv(r"C:\Users\parke\Documents\GitHub\EconCapstone\utils\CleanFinalDataNoOutliers.csv")
    print(df.columns)

    miner_unique_df = df.groupby('wallet_address').first()

    #print(miner_unique_df.head())

    size_description = miner_unique_df[' firm_size'].describe()
    age_description = miner_unique_df[' firm_age'].describe()
    print(size_description)
    print(age_description)

    print('fin')


def get_histoical_stats():

    df = pd.read_csv(r"C:\Users\parke\Documents\GitHub\EconCapstone\datasets\historical_data.csv")
    print(df.head())
    relevant_cols = df.columns
    for name in relevant_cols:
        try:
            average = round(df[name].mean(), 6)
            std_dev = round(df[name].std(), 6)
            print('Name: {} Average :{} std_dev: {}'.format(name, average, std_dev))

        except:
            print(name)


get_unique_miner_descriptive_stats()


# cut of the top and bot 1, 5% then see the percentiles.
# do this before the estimation.
# put the top and bot % off in the data section.
#