# floc-analysis

This repository contains the code and empirical results from our analysis about the privacy limitations of Google's FLoC proposal.

This analysis uses data from comScore Inc.
While our work is open source, the comScore data is proprietary and available for purchase and cannot be openly shared due to the terms of use. Our analysis shows aggregated previews of the data and can be fully replicated upon obtaining this dataset. 


## About FLoC

In 2021, Google announced they would disable third-party cookies in the Chrome browser in order to improve user privacy. They proposed FLoC as an alternative, meant to enable interest-based advertising while mitigating risks of individualized user tracking. The FLoC algorithm assigns users to k-anonymous "cohorts" that represent groups of users with similar browsing behaviors so that third-parties can serve users ads based on their group.

The FLoC API returns a users' cohort ID.

See https://github.com/WICG/floc


### FLoC algorithm

FLoC stands for "Federated Learning of Cohorts". However, despite the name, federated learning was not used in the implementation of FLoC.

Instead the FLoC algorithm used SimHash and PrefixLSH to sort user browser histories into cohorts guaranteed to be of minimum size k=2000. The algorithm is described in Google's KDD paper "Clustering for Private Interest-based Advertising" ([https://doi.org/10.1145/3447548.3467180](https://doi.org/10.1145/3447548.3467180)) and further details are provided in "[The FLoC Origin Trial & Clustering documentation](https://sites.google.com/a/chromium.org/dev/Home/chromium-privacy/privacy-sandbox/floc)".


### FLoC origin trial (OT)

Google tested their initial implementation of FLoC with a Chrome browser origin trial (OT) that millions (we estimate > 101,616,000) of eligible Chrome users were automatically included in.

Details have been published here: https://sites.google.com/a/chromium.org/dev/Home/chromium-privacy/privacy-sandbox/floc

- The OT ran in Chrome 89 to 91.
- The trial included Chrome users with at least 7 domains in their browsing history. 
- Cohorts had a minimum size of k=2000.
- 33,872 cohorts (before dropping sensitive cohorts).
- 2.3% of cohorts were deemed sensitive and dropped, desribed below.


Note:
- The SimHash value is computed over eTLD+1's from the browser's previous 7-day period (i.e. week) leading up to the cohort calculation.
- Cohorts are not generated for browsing data with fewer than 7 valid domains.

The way the FLoC API was implemented for the OT was: 
- A Google Chrome-operated server-side pipeline used synced Chrome user data to compute corresponding SimHash values, and sorted the SimHash values using PrefixLSH into the cohorts that were used in the OT.
- A file was then embedded into the Chrome browser that allowed browser instances to map SimHash values to cohort IDs.
- The SimHash algorithm was also included in the OT Chrome browser versions.
- This then enabled the FLoC API by allowing a local browser instance to compute its SimHash value using the recently browsed domains (eTLD+1s), and then look up its cohort ID using that hash value and the file that maps values to cohort IDs.


### Sensitive cohorts defined by Google using t-closeness and sensitive domains
The Google methodology for defining sensitivity and using t-closeness to determine sensitive cohorts is described in "[Measuring Sensitivity of Cohorts Generated by the FloC API](https://perma.cc/B95S-HKMG)".

Their implementation then "dropped" cohorts that violated t-closeness with t=0.1. A null cohort ID was returned by the FLoC API for browser instances in dropped cohorts.

We borrow their use of t-closeness in our sensitivity analysis, where sensitive cohorts are defined based on the racial backgrounds of cohort members.


## Our FLoC implementation

Our analysis could not directly use the cohort IDs (and hash value to cohort ID mapping) from the OT because our dataset represents a sample of user devices that is a small fraction of the size of the number of user devices used in the OT.
The OT cohort IDs were computed to be k-anonymous for k=2000 and there were 33,872 cohorts. If our analysis used these same cohorts, the cohorts would be sparsely populated, would not nearly reach the minimum size of k=2000, and the analysis would be meaningless.

Instead we re-implment the OT FLoC cohort computation to allow for varying levels of k.

To compute the SimHash over browsing histories in the same way as the FLoC OT, we use the SimHash implementation from the floc_simulator project that was developed by [@shigeki](https://github.com/shigeki): 
https://github.com/shigeki/floc_simulator.

This successfully replicated the cohort IDs seen in the Chrome browser, and was verified by Google's FLoC engineers.

We use a python wrapper for this FLoC simulator created by @thepabloaguilar: 
https://github.com/thepabloaguilar/floc.

We implemented FLoC PrefixLSH algorithm described in Google's KDD paper "Clustering for Private Interest-based Advertising" [https://doi.org/10.1145/3447548.3467180](https://doi.org/10.1145/3447548.3467180). 

Code:
[prefixLSH.py](prefixLSH.py)

Our FLoC cohort creation was further informed by the following resources in order to better match the FLoC OT:

- The FLoC Origin Trial & Clustering documentation: https://sites.google.com/a/chromium.org/dev/Home/chromium-privacy/privacy-sandbox/floc

- Clarifications made by Google FLoC engineers in https://github.com/WICG/floc/issues/


## Data sources

### The comScore Web Behavior Database

The comScore browsing sessions data was collected from more than 93,700 devices from 50,000 households across the U.S., over the 52 weeks of 2017. The sampled Internet users gave comScore explicit permission to confidentially capture their detailed browsing and buying behavior at the domain level.

Browsing sessions consist of a top-level domain name, associated statistics like number of pages viewed and duration of site visit, and the date of the visit. Each session is associated with a unique machine ID representing a single device in a U.S. household. Machine IDs are also associated with demographic information at the household level, which includes zip code and racial background. While a single household may have more than one machine, the dataset does not link the machine IDs by household; we treat machines as independent.

The included demographic data used in this analysis is race and zip code.

Our analyses that use racial background are limited by the racial backgrounds reported in the ComScore dataset, in which households are labeled as “Black”, “White”, “Asian”, or “Other”. We treat “Other” as being inclusive of multi-racial households and households that identify as Latino or Hispanic.

A description of the comScore data is in [data/comscore/2017/codebook.pdf](data/comscore/2017/codebook.pdf)


### Census data

We use census data from the American Community Survey (ACS) in order to inspect the representativeness of the comScore dataset and compute panels representative of the U.S. population for use in our sensitivity analysis.


## Anaylysis steps

### Pre-analysis: Demographics

We compare the demographics to census data from the same time period.
We find that the distributions of populations by state and race demographics are very similar, but the distributions of other demographics are not.

We also learn about the data quirks and bad encodings to work around in the preprocessing steps.

[notebooks/check-comscore-demographics.ipynb](notebooks/check-comscore-demographics.ipynb)


### Sessions data preprocessing

We filter out raw sessions data records with invalid eTLD+1s (domains).

We genenerate a preprocessed file representing the unique domains visited by each machine_id for each week (i.e. 7-day period). This data is used as input for the FLoC algorithm to compute weekly cohort IDs for each machine, for each week.

Code:
[notebooks/domains_preprocessing_by_week_machine.ipynb](notebooks/domains_preprocessing_by_week_machine.ipynb)

Output table columns:
```
machine_id, week, n_domains, domains_str
```

Where
- domains_str is the set of unique domains visited by the machine_id in the week
- n_domains is the number of unique domains in domains_str

We refer to the rows in this table as machine-weeks.


### Unicity analysis

Since cohorts are computed based on the previous 7-day period of browsing history, a user device's cohort ID may change from week to week.

While cohorts are designed to be k-anonymous, the sequence of cohort IDs for a user device computed across weeks may be unique, and could then be used by third-parties to uniquely identify and track users across sites. Such a privacy risk would be contrary to the FLoC privacy goals of mitigating the risks of individualized user tracking. 

Is this a risk? 
If so, how many weeks (cohort IDs in a sequence) until this risk of unicity presents itself?
How does this risk increase when cohort IDs are combined with other forms of browser fingerprinting?

We analyze these questions using the preprocessed machine-weeks data.

[notebooks/notebooks/unicity-analysis.ipynb](notebooks/notebooks/unicity-analysis.ipynb)


### Sensitivity analysis

A core question in our analysis is whether information about a device user's likely race can be leaked by their FLoC cohort.

#### Relationship between racial background and domain browsing

We do initial analysis of the relationship between racial background and domain browsing using the preprocessed machine-weeks data.

[notebooks/sensitivity-by-race-by-domain-visit-frequency.ipynb](notebooks/sensitivity-by-race-by-domain-visit-frequency.ipynb)


#### t-closeness

##### Checking t-closeness violations for panel size matching OT

As a first preliminary check, we check t-closeness violations with an artificially constructed panel that matches the U.S. population w.r.t. racial background distribution (using 2019 census data) and where cohort IDs are randomly assigned, and where the size of the panel is close to the FLoC size.

We do this because if we find that random cohort ID assignments do not violate t-closeness (t=0.1, used in the OT) for the OT, and also find using our smaller dataset that FLoC cohort ID assignments do not violate t-closeness anymore than random change, then we can assume that the FLoC OT would not violate t-closeness.

We find t-closeness is not violated for this panel (t=0.1).

[notebooks/t-closeness-for-us-race.ipynb](notebooks/t-closeness-for-us-race.ipynb)


##### Panel creation via stratified sampling

Panels are sampled using stratified random sampling (without replacement) so that the distribution of race demographics in each of the panels matches the distribution of the U.S. population, as reported by the Census (ACS).

We generate 10 panels for each of the 520 weeks.

This allows us to compute confidence intervals in our t-closeness analysis.

The output of this step is a panels file that is then used in the following steps.

[generate-stratified-panels-by-race-for-week-machine.ipynb](generate-stratified-panels-by-race-for-week-machine.ipynb)


##### Precompute SimHash for panels and create randomized panel

We precompute the SimHash values for each machine-week for each panel sample.
We then precompute the cohort assignments for each panel for use in the t-closeness analysis.

We also create a randomized version of the panel to use as a comparison baseline. To do this, we copy the panels and randomly shuffle the SimHash values and compute cohorts. For this new randomized panel where the SimHash values have been randomly reassigned, race for panel samples is guaranteed independent of cohort assignment.

[notebooks/cohorts-for-comscore-race-stratified-panels.ipynb](notebooks/cohorts-for-comscore-race-stratified-panels.ipynb)


##### t-closeness analysis using precomputed panels

We compute t-closeness violations, where race is considered the sensitive attribute, over our panels data for a range of t values.

Since our panels are small, some t-closeness violations must be expected due to random chance.
We compare the empirical results from our panels data to two baselines that represent t-closeness violations due to random chance:
1. expected t-closeness violations modeled by a binomial CDF.
2. t-closeness violations computed over the randomized panels data.

[notebooks/t-closeness-for-comscore-panels-by-race.ipynb](notebooks/t-closeness-for-comscore-panels-by-race.ipynb)
