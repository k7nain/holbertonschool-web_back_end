#!/usr/bin/env python3
"""Module that contains function sum_mixed_list"""
from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:

    """Returns the sum of a mixed list of ints and floats"""
    return float(sum(mxd_lst))
