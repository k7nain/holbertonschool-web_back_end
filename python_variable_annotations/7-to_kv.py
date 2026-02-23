#!/usr/bin/env python3
"""Module that contains function to_kv"""
from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:

    """Returns a tuple (k, v squared as float)"""
    return (k, float(v ** 2))
