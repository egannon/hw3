# -*- coding: utf8 -*-
from __future__ import unicode_literals
import unittest
import sys 

import avl 

if sys.version_info[0] == 3:
    unicode = str

class AvlTest1(unittest.TestCase):

    def test1(self):
        tree = avl.AVL() 
        tree.insert(8) 
        tree.insert(6) 
        tree.insert(7) 
        tree.insert(5) 
        tree.insert(3) 
        tree.insert(0) 
        tree.insert(9) 
        result = tree.find_min() 
        self.assertEqual(result.key, 0) 


unittest.main()         # run all tests
