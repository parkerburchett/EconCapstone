import statsmodels.api as sm
import numpy as np
import pandas as pd

#https://www.statsmodels.org/stable/index.html

#https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.OLS.html
# source: https://www.datarobot.com/blog/multiple-regression-using-statsmodels/



def main():
    df = pd.read_csv(r"C:\Users\parke\Documents\GitHub\EconCapstone\utils\CleanFinalDataNoOutliers.csv")
    print(df.columns)
    dependent_variables = df[[' firm_age',' firm_size',' prev_month_GHs_value', ' prev_prev_month_GHs_value']]
    independent_variable = df[' GHs_elasticity']

    est = sm.OLS(independent_variable,dependent_variables).fit()
    print(type(est))

    print(est.summary())
    print(est.params)
    for i in range(4):
        print(est.pvalues[i])

def calc_corrilations():
    print(df.columns)
    # might need to exclude start date since it is not an number.
    pd.set_option('display.max_columns', None)

    df.corr(method='pearson').to_csv('corrilation_result.csv')

def sample_data():
    df = pd.read_csv(r'C:\Users\parke\Documents\GitHub\EconCapstone\utils\sample_health_data.csv')

    x1 = 'DeathRatePer1000Residents'
    x2 = 'doctor availability per 100000'
    x3 = 'hospital availability per 100000'
    x4 = 'annual per capita income'
    x5 = 'population density per square mile'
    header = [x1,x2,x3,x4,x5]
    df.columns = header
    #
    #print(df.head())
    X = df[['population density per square mile', 'doctor availability per 100000']]
    y = df['DeathRatePer1000Residents']

    est = sm.OLS(y, X).fit()
    print(est.summary())


    # R^2 is the portion of total variation that is explained by the model.

main()



