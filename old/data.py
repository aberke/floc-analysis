import pandas as pd
import numpy as np


def read_comscore_demo_df(year, fpath='data/comscore/{year}/demographics.csv'):
    demographics_fpath = fpath.format(year=year)
    demo_df = (pd.read_csv(demographics_fpath, usecols=['household_income', 'racial_background', 'machine_id'])
               .assign(household_income = lambda x: x.household_income % 10)
               .replace({99:np.nan, -88: np.nan, 8: np.nan})
              .dropna())
    return demo_df


def read_cps_df(fpath="data/CPS-race.csv"):
    cps_df = pd.read_csv(fpath, usecols=[0,1,2,3,4])[1:]
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


# ------------------------------------------------------------------------------
def write_weeks_machines_domains(df, weeks_machines_domains_fpath):
    df['domains_str'] = df.domains.apply(lambda x: "|".join(x))
    print('saving %s rows to file %s...' % (len(df), weeks_machines_domains_fpath))
    df.drop('domains', axis=1).to_csv(weeks_machines_domains_fpath, index=False)
    print('...saved')
    
def read_weeks_machines_domains(weeks_machines_domains_fpath, nrows=None):
    print('reading from %s...' % weeks_machines_domains_fpath)
    df = pd.read_csv(weeks_machines_domains_fpath, nrows=nrows)
    df['domains'] = df.domains_str.fillna('').apply(lambda x: set(x.split('|')) if x else set())
    df.drop('domains_str', axis=1, inplace=True)
    print('... read %s rows' % len(df))
    return df