#!/usr/bin/env python3
"""
BasicCache module - implements a basic caching system.
"""

from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """
    BasicCache - has no limit on the number of items it can store.
    """

    def put(self, key, item):
        """
        Add an item in the cache.
        """
        if key is None or item is None:
            return
        self.cache_data[key] = item

    def get(self, key):
        """
        Get an item from the cache.
        """
        return self.cache_data.get(key, None)
