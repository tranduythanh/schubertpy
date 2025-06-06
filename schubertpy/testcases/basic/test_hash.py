import unittest
from schubertpy.utils.hash import hashable_lru_cache, hashable_lru_cache_method

class TestHashableLruCache(unittest.TestCase):
    def test_function_caching_lists(self):
        calls = {'count': 0}

        @hashable_lru_cache(maxsize=2)
        def foo(x):
            calls['count'] += 1
            return sum(x)

        self.assertEqual(foo([1, 2, 3]), 6)
        self.assertEqual(foo([1, 2, 3]), 6)
        self.assertEqual(calls['count'], 1)
        self.assertEqual(foo([2, 2]), 4)
        self.assertEqual(calls['count'], 2)

class Dummy:
    def __init__(self):
        self.calls = 0

    @hashable_lru_cache_method(maxsize=2)
    def bar(self, values):
        self.calls += 1
        return sum(values)

class TestHashableLruCacheMethod(unittest.TestCase):
    def test_method_caching_lists(self):
        d = Dummy()
        self.assertEqual(d.bar([1, 1]), 2)
        self.assertEqual(d.bar([1, 1]), 2)
        self.assertEqual(d.calls, 1)
        self.assertEqual(d.bar([0, 1]), 1)
        self.assertEqual(d.calls, 2)

if __name__ == '__main__':
    unittest.main()
