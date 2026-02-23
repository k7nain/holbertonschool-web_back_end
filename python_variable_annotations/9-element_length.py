#!/usr/bin/env python3
"""Module that contains function element_length"""
from typing import Iterable, Sequence, List, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:

    """Returns a function length"""
    return [(i, len(i)) for i in lst]
