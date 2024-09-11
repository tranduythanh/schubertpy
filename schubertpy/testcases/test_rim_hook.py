from ..partition import Partition
import unittest

class TestPartition(unittest.TestCase):
    
    def test_remove_rim_hooks_1(self):
        p = Partition([7,3])
        result = p.remove_rim_hooks(7, (3, 4))
        self.assertEqual(result.partition, [2,1])

    def test_remove_rim_hooks_2(self):
        p = Partition([7,2, 1])
        result = p.remove_rim_hooks(7, (3, 4))
        self.assertEqual(result.partition, [1,1,1])
    
    def test_remove_rim_hooks_3(self):
        p = Partition([6,4])
        result = p.remove_rim_hooks(7, (3, 4))
        self.assertEqual(result.partition, [3])
    
    def test_remove_rim_hooks_4(self):
        p = Partition([6,3,1])
        result = p.remove_rim_hooks(7, (3, 4))
        self.assertEqual(result.partition, [])
    
    def test_remove_rim_hooks_5(self):
        p = Partition([6,2,2])
        result = p.remove_rim_hooks(7, (3, 4))
        self.assertEqual(result.partition, [1,1,1])

    def test_remove_rim_hooks_6(self):
        p = Partition([5,4,1])
        result = p.remove_rim_hooks(7, (3, 4))
        self.assertEqual(result.partition, [3])

    def test_remove_rim_hooks_7(self):
        p = Partition([5,3,2])
        result = p.remove_rim_hooks(7, (3, 4))
        self.assertEqual(result.partition, [2,1])
    
    def test_remove_rim_hooks_8(self):
        p = Partition([5,5])
        result = p.remove_rim_hooks(5, (2, 3))
        self.assertEqual(result.partition, [])
