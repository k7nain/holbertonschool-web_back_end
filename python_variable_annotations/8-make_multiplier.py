#!/usr/bin/env python3
"""Module that contains function make_multiplier"""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:

    """Returns a function that multiplies a float by multiplier"""
    def multiply(x: float) -> float:
        return x * multiplier
    return multiply
