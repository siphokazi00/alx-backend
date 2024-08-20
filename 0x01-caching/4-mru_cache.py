#!/usr/bin/env python3
"""
MRUCache module - implements an MRU caching system.
"""

from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """
    MRUCache - follows the MRU algorithm.
    """

    def __init__(self):
        """ Initialize the MRU cache system """
        super().__init__()
        self.mru_key = None

    def put(self, key, item):
        """
        Add an item in the cache.
        """
        if key is None or item is None:
            return

        if len(self.cache_data) >= BaseCaching.MAX_ITEMS and key not in self.cache_data:
            if self.mru_key is not None:
                del self.cache_data[self.mru_key]
                print(f"DISCARD: {self.mru_key}")

        self.cache_data[key] = item
        self.mru_key = key

    def get(self, key):
        """
        Get an item from the cache.
        """
        if key in self.cache_data:
            self.mru_key = key
            return self.cache_data.get(key)
        return None
