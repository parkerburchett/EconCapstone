import pandas as pd

def main():
    df = pd.read_csv(r"C:\Users\parke\Documents\GitHub\EconCapstone\utils\CleanFinalDataNoOutliers.csv")


    relevant_cols = [' firm_size',' firm_age', ' eth_earned_this_month', ' GHs_elasticity',]

    print('DESCRIPTIVE STATS ON GH/S ELASTICITY')
    print(df[' GHs_elasticity'].describe(percentiles=[.01,.05,.1,.2,.3,.4,.5,.6,.7,.8,.9,.95,.99]).apply(lambda x: format(x, 'f')))
    print('median', df[' GHs_elasticity'].median())

    for name in relevant_cols:
        average = round(df[name].mean(),6)
        std_dev = round(df[name].std(),6)
        print('Name: {} Average :{} std_dev: {}'.format(name,average,std_dev))


main()


# cut of the top and bot 1, 5% then see the percentiles.
# do this before the estimation.
# put the top and bot % off in the data section.
#