# floc-analysis

This repository contains the code and empirical results from our analysis about the privacy limitations of Google's FLoC proposal.

This analysis uses data from comScore Inc.
While our work is open source, the comScore data is proprietary and available for purchase and cannot be openly shared. Our analysis shows aggregated previews of the data and can be fully replicated upon obtaining this dataset. 


## Data sources

### The comScore Web Behavior Database

The comScore browsing sessions data was collected from more than 93,700 devices from 50,000 households across the U.S., over the 52 weeks of 2017. The sampled Internet users gave comScore explicit permission to confidentially capture their detailed browsing and buying behavior at the domain level.

The unique identifier is Machine ID and there are cases where multiple configured machines exist within a household, but all demographic information is based upon the associated household. All sessions are aggregated by machine in the household and a particular individual could use more than one machine.

A description of the comScore data is in data/comscore/2017/codebook.pdf

### Census data

We use census data from the American Community Survey (ACS) in order to inspect the representativeness of the comScore dataset and compute panels representative of the U.S. population for use in our sensitivity analysis.


## Anaylysis steps

### Pre-analysis

We compare the demographics to census data from the same time period.
See notebook: https://github.com/aberke/floc-analysis/blob/master/notebooks/demographics_explore.ipynb

We find that the distributions of populations by state and race demographics are very similar, but the distributions of other demographics are not.

### Panel creation via stratified sampling

The output of the panel creation step is N panels, where each panel is randomly sampled without replacement, as described below. Output: `output/all_panels.csv` 

Current Population Survey (CPS) data is used with a stratified sampling approach to create panel data where the proportion of race, income groups are representative of nationwide U.S. demographics.
(The Total > All Races table is used from https://www.census.gov/data/tables/time-series/demo/income-poverty/cps-hinc/hinc-02.2017.html.)
(Income groups are collapsed.)

To create a panel, combinations of `machine_id, week` are randomly sampled without replacement such that the demographics associated with the `machine_id`s in the panel are representative of the CPS data.

Each `machine_id` is associated with its household demographics. Each `week` represents a week of browsed domains for that `machine_id`.
Each week of data is considered an independent sample.


### Panel domain history

Output:

Each `machine_id, week` is connected to its list of domains.


`machine_id, week` --> `machine_id, week, domain1.com|domain2.com|domain3.com`

TODO: describe how the list of domains for the samples of `machine_id, week` are generated and associated with samples.


### FLoC simulation to generate cohorts

Output: TODO

Each `machine_id, week` sample in the panel is associated with a cohort ID. The cohort ID is determined by using the week of browsed domains.
The domains are used as input for the floc_simulator written by @shigeki.
https://github.com/shigeki/floc_simulator. 
We use an already written python wrapper for this FLoC simulator: 
https://github.com/thepabloaguilar/floc.


### FLoC cohort analysis


