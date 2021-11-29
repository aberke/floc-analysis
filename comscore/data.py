import pandas as pd
import numpy as np


def read_comscore_demo_df(year):
    demographics_fpath = 'data/comscore/{year}/demographics.csv'.format(year=year)
    demo_df = (pd.read_csv(demographics_fpath, usecols=['household_income', 'racial_background', 'machine_id'])
               .assign(household_income = lambda x: x.household_income % 10)
               .replace({99:np.nan, -88: np.nan, 8: np.nan})
              .dropna())
    return demo_df


def read_cps_df():
    cps_df = pd.read_csv("data/CPS-race.csv", usecols=[0,1,2,3,4])[1:]
    # manually created mapping from CPS categories to comscore levels.
    cps_df['comscore_mapping'] = [1,1,1,2,2,3,3,4,4,4,5,5,5,5,5,6,6,6,6,6,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7]
    cps_df = (cps_df.drop('Unnamed: 0', axis=1)
              # convert formatted numbers to numbers
              .apply(lambda x: pd.to_numeric(x.astype(str).str.replace(",", "")))
              .rename(columns={'white alone': 1,
                              'black alone': 2,
                              'asian alone': 3})
             )
    # Comscore only uses white,black,asian so we sum across these identities and subtract
    # the total to get the 'other' count also present in the comscore data
    cps_df['5'] = cps_df.total - cps_df[[1,2,3]].sum(axis=1)
    return cps_df.drop('total', axis=1)


