'''
Created on Apr 9, 2012

@author: mdoan
'''

import pymongo


class ProductsManager:
    """
    the manager system organizes the products
    """
    def __init__(self):
        self._db = pymongo.Connection().products
        self._purchased = self._db.purchased
        
    def add(self, prod1_name, prod2_name, times):
        try:
            """
            add a new pair of products with times purchased together
                - if the pair existed, just increase the times purchased
                - otherwise just add the new pair
            """
            self._purchased.update({'prod1': prod1_name, 'prod2': prod2_name, 'times': {'$exists': True}},
                                   {'$inc': {'times': times}},
                                   True
                                   )
        except Exception as ex:
            print(ex.value) 
        
pm = ProductsManager()
pm.add('2', '6', 5)
