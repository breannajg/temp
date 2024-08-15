import os
import unittest 
 
class TestDummy(unittest.TestCase): 
  '''
  An Object containing a collection of tests
  '''

  def test_one(self):
    '''
    An empty test
    '''
    self.assertTrue(True)
 
if __name__ == '__main__': 
  unittest.main() 
