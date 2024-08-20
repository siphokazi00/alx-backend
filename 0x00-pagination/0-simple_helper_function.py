#!/usr/bin/env python3
"""
Provides a function to calculate pagination indices
"""


def index_range(page: int, page_size: int) -> tuple:
    """
    Calculate the start and end indices for a given page and page size.
    """
    start_index = (page - 1) * page_size
    end_index = page * page_size
    return (start_index, end_index)
