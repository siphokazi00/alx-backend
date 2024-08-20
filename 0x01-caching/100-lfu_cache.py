#!/usr/bin/env python3
"""
LFUCache module - implements an LFU caching system with LRU tie-breaker.
"""

from base_caching import BaseCaching
from collections import defaultdict, OrderedDict


class LFUCache(BaseCaching):
    """
    LFUCache - follows the LFU algorithm.
    """

    def __init__(self):
        """ Initialize the LFU cache system """
        super().__init__()
        self.frequency = defaultdict(int)
        self.usage_order = OrderedDict()

    def put(self, key, item):
        """
        Add an item in the cache.
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
            self.frequency[key] += 1
            self.usage_order.move_to_end(key)
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                min_freq = min(self.frequency.values())
                least_freq_keys = [k for k, v in self.frequency.items() if v == min_freq]

                if len(least_freq_keys) > 1:
                    lfu_key = next(k for k in self.usage_order if k in least_freq_keys)
                else:
                    lfu_key = least_freq_keys[0]

                del self.cache_data[lfu_key]
                del self.frequency[lfu_key]
                del self.usage_order[lfu_key]
                print(f"DISCARD: {lfu_key}")

            self.cache_data[key] = item
            self.frequency[key] = 1
            self.usage_order[key] = None

    def get(self, key):
        """
        Get an item from the cache.
        """
        if key in self.cache_data:
            self.frequency[key] += 1
            self.usage_order.move_to_end(key)
            return self.cache_data[key]
        return None
