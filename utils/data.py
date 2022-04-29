import pandas as pd
import numpy as np


# The comscore data is coded with 8 income groups.
# The Census data is code with many more. We used 4
# income groups that both census and comScore data can map to. 
income_groups_4 = {
    1: 'less than $25,000',
    2: '\$25,000 - $75,000',
    3: '\$75,000 - $150,000',
    4: '\$150,000 or more',
 }
 # comscore data is coded as follows. We add in 'any'.
race_groups = {
    1: 'white', 
    2: 'black', 
    3: 'asian', 
    5: 'other', 
    'any': 'any',
}


def read_comscore_demo_df(year, fpath='data/comscore/{year}/demographics.csv'):
    demographics_fpath = fpath.format(year=year)
    demo_df = (pd.read_csv(demographics_fpath, usecols=['household_income', 'racial_background', 'machine_id'])
               .replace({99:np.nan, -88: np.nan})
              .dropna())
    return demo_df


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