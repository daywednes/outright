'''
Created on Apr 11, 2012

@author: mdoan
'''
import unittest

class Test(unittest.TestCase):

    def setUp(self):
        from outright.core.products import ProductsManager
        self._pm = ProductsManager() 


    def tearDown(self):
        del self._pm

    def test_add_assign(self):
        self._pm.assign(1, 2, 3)
        self.assertEqual(self._pm.get_times(1, 2), 3)
        self.assertEqual(self._pm.get_times(2, 1), 3)
        self._pm.add(1, 2, 3)
        self.assertEqual(self._pm.get_times(1, 2), 6)
    def test_remove(self):
        self._pm.remove(1, 2)
        self.assertEqual(self._pm.get_times(2, 1), None)
    def test_add_products(self):
        prod_list = []
        with open('products.txt') as f:
            for line in f:
                prod_list.append(tuple(map(int, line.split())))
            self.assertEqual(True, self._pm.insert_product_list(prod_list))
        
    def test_recommend_next_product(self):
        self._pm.clear()
        print(self._pm.recommend_next_product([1, 33, 22]))
        
        

def create_a_test():
    import random
    random.seed()
    with open('products.txt', 'w') as f:
        for _ in range(1000000):
            print(random.randint(1, 1000), random.randint(1, 1000), random.randint(1, 100), file = f)
            
if __name__ == "__main__":
#    create_a_test()
    import sys;sys.argv = ['', 'Test.testAdd_Assign']
    
    unittest.main()