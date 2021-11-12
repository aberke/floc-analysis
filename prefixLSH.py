# prefixLSH.py

import numpy as np


MAX_NUMBER_BITS_IN_FLOC = 50
K = 50


def binary_hash(h):
    return np.binary_repr(h, width=MAX_NUMBER_BITS_IN_FLOC)


def get_cohorts_dict(hash_list, min_k=K):
    """
    Applies the prefixLSH algorithm described in paper 
    "Clustering for Private Interest-based Advertising" by Epasto and Medina, et al.

    Args:
    hash_list - a list of hashes to sort, where the hashes are *not* bit arrays.
    min_k - the minimum number of hashes that can be in a cohort.

    Returns a dictionary mapping hash to (int) cohort ID.
    """
    # map hashes to their bit array representations
    bit_hash_map = {h: binary_hash(h) for h in hash_list}
    # pass list with duplicates to sorting algorithm instead of values of map
    bit_hash_list = [binary_hash(h) for h in hash_list] 
    bit_hash_cohorts_dict = get_bit_hash_cohorts_dict(bit_hash_list)
    # map back to non bit-array hashes
    return {h: bit_hash_cohorts_dict[binary_hash(h)] for h in hash_list}


def get_bit_hash_cohorts_dict(bit_hash_list, min_k=K):
    """
    Applies the prefixLSH algorithm described in paper 
    "Clustering for Private Interest-based Advertising" by Epasto and Medina, et al.

    Args:
    bit_hash_list - a list of hashes to sort where the hashes are bit arrays.
    min_k - the minimum number of hashes that can be in a cohort.

    Returns a dictionary mapping hash to (int) cohort ID.
    """
    sorted_bit_hash_list = sorted(bit_hash_list)
    return apply_prefixLSH({}, 0, sorted_bit_hash_list, min_k=min_k)


def apply_prefixLSH(cohorts_dict, bit, sorted_bit_hash_list, min_k):

    """
    pre-order tree traversal. Each leaf corresports to a cohort ID.
    """
    if len(sorted_bit_hash_list) < min_k:
        raise Exception("fewer than %s hashes to sort" % min_k)
    if bit == MAX_NUMBER_BITS_IN_FLOC:
        raise Exception("maximum number of bits exceeded: %s" % bit)
    # all items in hash list must be same length/number of bits
    if not all(len(sorted_bit_hash_list[0]) == len(s) for s in sorted_bit_hash_list):
        raise Exception("items in hash list of different lengths")
    # search through sorted hash list at bit=bit for the first hash where bit=1
    # start at 1 less than minimum k. If all have bit=1, then left list will be too small
    i = min_k - 1
    if bit < len(sorted_bit_hash_list[0]):
        while i < len(sorted_bit_hash_list):
            if sorted_bit_hash_list[i][bit] == "1":
                break
            i += 1
    left_sorted_bit_hash_list = sorted_bit_hash_list[:i]
    right_sorted_bit_hash_list = sorted_bit_hash_list[i:]

    if (len(left_sorted_bit_hash_list) < min_k) or (len(right_sorted_bit_hash_list) < min_k):
        # Do not recurse. This is a cohort.
        # cohort ID is the next largest cohort ID that hasn't been assigned.
        cohort_id = max(cohorts_dict.values()) + 1 if cohorts_dict else 1
        cohorts_dict.update({bit_hash:cohort_id for bit_hash in sorted_bit_hash_list})
        return cohorts_dict

    cohorts_dict = apply_prefixLSH(cohorts_dict, bit+1, left_sorted_bit_hash_list, min_k)
    cohorts_dict = apply_prefixLSH(cohorts_dict, bit+1, right_sorted_bit_hash_list, min_k)
    return cohorts_dict
