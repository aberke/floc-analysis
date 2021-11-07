import pandas as pd
import numpy as np
from datetime import datetime
import random
from .utils.stratify import stratify_data_without_replacement
from .data import read_cps_df, read_comscore_demo_df


def stratify_cps(cps_df):
    return (
        cps_df.groupby("comscore_mapping")
        .agg(sum)
        .melt(ignore_index=False)
        .reset_index()
        .astype(float)
        .assign(
            stratify=lambda x: x.comscore_mapping.astype(str)
            + ", "
            + x.variable.astype(str)
        )[["stratify", "value"]]
        .set_index("stratify")
        .assign(value=lambda x: x.value / sum(x.value))
    ).value


def generate_stratified_sample(cps_df, comscore_demo_df, seed_value=datetime.now()):
    random.seed(seed_value)
    cps_stratify = stratify_cps(cps_df)
    demo_df_s = stratify_data_without_replacement(
        comscore_demo_df, "stratify", cps_stratify.index, cps_stratify.values
    )

    demo_stratified = demo_df_s.stratify.value_counts()
    # summary dataframe between stratified source and our dataset
    # summary_df = (
    #     pd.DataFrame(demo_stratified / demo_stratified.sum())
    #     .merge(cps_stratify, left_index=True, right_index=True)
    #     .rename(columns={"stratify": "comscore_proportion", "value": "cps_proportion"})
    # )
    return demo_df_s
