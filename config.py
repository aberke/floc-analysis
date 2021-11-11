CENSUS_YEAR = 2017
COMSCORE_YEAR = 2017
N_PANELS = 500
N_CORES = 8

# income mapping for aggregating ComScore data to fewer
# categories so stratification creates larger panels
INCOME_MAPPING = {
    # 1 is 0 to 25k 
    # 2 is 25k to 50k
    # 3 is 50k to 100k
    # 4 is 100k +
    1: 1, # less than 10k and 10k-15k
    2: 1, # 15-25k
    3: 2, # 25-35k
    4: 2, # 35-50k
    5: 3, # 50-75k
    6: 3, # 75-100k
    7: 4, # 100k+
}