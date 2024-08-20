#!/usr/bin/env python3
"""
LIFOCache module - implements a LIFO caching system.
"""

from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """
    LIFOCache - follows the LIFO algorithm.
    """

    def __init__(self):
        """ Initialize the LIFO cache system """
        super().__init__()
        self.last_key = None

    def put(self, key, item):
        """
        Add an item in the cache.
        """
        if key is None or item is None:
            return

        if len(self.cache_data) >= BaseCaching.MAX_ITEMS and key not in self.cache_data:
            if self.last_key is not None:
                del self.cache_data[self.last_key]
                print(f"DISCARD: {self.last_key}")

        self.cache_data[key] = item
        self.last_key = key

    def get(self, key):
        """
        Get an item from the cache.
        """
        return self.cache_data.get(key, None)
