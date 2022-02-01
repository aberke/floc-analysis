import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def stratify_data_with_replacement(
    df_data,
    stratify_column_name,
    stratify_values,
    stratify_proportions,
    random_state=None,
):
    """Stratifies data according to the values and proportions passed in
    from: https://gist.github.com/grahamharrison68/9223f4e80bb2c553b3a31be3b7c854b5#file-stratify_4-py
    Args:
        df_data (DataFrame): source data
        stratify_column_name (str): The name of the single column in the dataframe that holds the data values that will be used to stratify the data
        stratify_values (list of str): A list of all of the potential values for stratifying e.g. 'Male, Graduate', 'Male, Undergraduate', 'Female, Graduate', 'Female, Undergraduate'
        stratify_proportions (list of float): A list of numbers representing the desired propotions for stratifying e.g. 0.4, 0.4, 0.2, 0.2, The list values must add up to 1 and must match the number of values in stratify_values
        random_state (int, optional): sets the random_state. Defaults to None.
    Returns:
        DataFrame: a new dataframe based on df_data that has the new proportions represnting the desired strategy for stratifying
    """

    df_stratified = pd.DataFrame( columns=df_data.columns)  # Create an empty DataFrame with column names matching df_data

    pos = -1
    for i in range(
        len(stratify_values)
    ):  # iterate over the stratify values (e.g. "Male, Undergraduate" etc.)
        pos += 1
        if pos == len(stratify_values) - 1:
            ratio_len = len(df_data) - len(
                df_stratified
            )  # if this is the final iteration make sure we calculate the number of values for the last set such that the return data has the same number of rows as the source data
        else:
            ratio_len = int(
                len(df_data) * stratify_proportions[i]
            )  # Calculate the number of rows to match the desired proportion

        df_filtered = df_data[
            df_data[stratify_column_name] == stratify_values[i]
        ]  # Filter the source data based on the currently selected stratify value
        df_temp = df_filtered.sample(
            replace=True, n=ratio_len, random_state=random_state
        )  # Sample the filtered data using the calculated ratio

        df_stratified = pd.concat(
            [df_stratified, df_temp]
        )  # Add the sampled / stratified datasets together to produce the final result

    return df_stratified  # Return the stratified, re-sampled data


def stratify_data_without_replacement(
    df_data,
    stratify_column_name,
    stratify_values,
    stratify_proportions,
    random_state=None,
):
    df_stratified = pd.DataFrame(columns=df_data.columns)
    max_idx = np.argmax(stratify_proportions)
    max_N = len(df_data[df_data[stratify_column_name] == stratify_values[max_idx]])
    true_N = (stratify_proportions / stratify_proportions[max_idx]) * max_N

    for i, N in enumerate(true_N):
        df_resampled = df_data[
            df_data[stratify_column_name] == stratify_values[i]
        ].sample(replace=False, n=int(N), random_state=random_state)
        df_stratified = pd.concat([df_stratified, df_resampled])
    return df_stratified
