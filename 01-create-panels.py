#!/usr/bin/env python
import pandas as pd
from config import N_PANELS, COMSCORE_YEAR, N_CORES
from comscore.data import read_cps_df, read_comscore_demo_df
from comscore.panel import generate_stratified_sample
from joblib import Parallel, delayed

print("Reading CPS and comscore data...")
cps_df = read_cps_df()
comscore_demo_df = read_comscore_demo_df(year=COMSCORE_YEAR)

print("Done. Generating panels...")



panels = Parallel(n_jobs=N_CORES)(delayed(generate_stratified_sample)(cps_df, comscore_demo_df,
    seed_value=n) for n in range(N_PANELS))

print("Done. Assigning panel IDs and writing to disk...")

panels = [p.assign(panel_id=n) for n, p in enumerate(panels)]
all_panels = pd.concat(panels).reset_index(drop=True)
all_panels.to_csv('output/all_panels.csv')
