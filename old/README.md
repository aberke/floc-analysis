# What is old

In a earlier version of this work we stratified on both race and household income, by using these demographic variables from the comScore data and from CPS data.

### Panel creation via stratified sampling

The output of the panel creation step is N panels, where each panel is randomly sampled without replacement, as described below. Output: `output/all_panels.csv` 

Current Population Survey (CPS) data is used with a stratified sampling approach to create panel data where the proportion of race, income groups are representative of nationwide U.S. demographics.
(The Total > All Races table is used from https://www.census.gov/data/tables/time-series/demo/income-poverty/cps-hinc/hinc-02.2017.html.)
(Income groups are collapsed.)

To create a panel, combinations of `machine_id, week` are randomly sampled without replacement such that the demographics associated with the `machine_id`s in the panel are representative of the CPS data.

Each `machine_id` is associated with its household demographics. Each `week` represents a week of browsed domains for that `machine_id`.
Each week of data is considered an independent sample.