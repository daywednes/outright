'''
Created on Apr 9, 2012

@author: mdoan
'''
import pymongo.errors as pyerrors
from collections import defaultdict 
import pymongo
import math
import operator


PROD1 = 'prod1'
PROD2 = 'prod2'
TIMES = 'times'

class ProductsManager:
    """
    The manager system organizes the products
    """

    def __init__(self):
        self._db = pymongo.Connection().products
        self._purchased = self._db.purchased
        
    def add(self, prod1_name, prod2_name, times):
        """
        Add a new pair of products with times purchased together
            - if the pair existed, just increase the times purchased
            - otherwise just add the new pair
        """
        if prod1_name == prod2_name:
            return
        try:
            self._purchased.update({PROD1: prod1_name, PROD2: prod2_name, TIMES: {'$exists': True}},
                                   {'$inc': {TIMES: times}},
                                   True
                                   )
            self._purchased.update({PROD1: prod2_name, PROD2: prod1_name, TIMES: {'$exists': True}},
                                   {'$inc': {TIMES: times}},
                                   True
                                   )
            print('add: succeeded')
            return True
        except pyerrors.OperationFailure as ex:
            print(ex.value)
        except pyerrors.PyMongoError as ex:
            print(ex.value)
        print('add: failed')
        return False

    def insert_product_list(self, prod_list):
        """
        Insert a list of pairs of products
        """
        try:
            json_list = []
            for item in prod_list:
                json_list.append({PROD1: item[0], PROD2: item[1], TIMES: item[2]})
                json_list.append({PROD1: item[1], PROD2: item[0], TIMES: item[2]})
                if len(json_list) > 20000:
                    self._purchased.insert(json_list)
                    del json_list[:]
                    print('just inserted another 20000 items')
            print('insert_product_list: succeeded')
            return True
        except pyerrors.OperationFailure as ex:
            print(ex.value)
        except pyerrors.PyMongoError as ex:
            print(ex.value)
        print('insert_product_list: failed')
        return False
    
    def add_product_list(self, prod_list):
        """
        Add a list of pairs of products one by one
        """
        success = True
        for item in prod_list:
            success &= self.add(item[0], item[1], item[2])
        if success: print('add_product_list: succeeded')
        else: print('add_product_list: failed')
        
        return success
            
    def remove(self, prod1_name, prod2_name): 
        """
        Remove a pair of products
        """
        try:
            self._purchased.remove({PROD1: prod1_name, PROD2: prod2_name},
                                   True
                                   )
            self._purchased.remove({PROD1: prod2_name, PROD2: prod1_name},
                                   True
                                   )
            print('remove: succeeded')
            return True
        except pyerrors.OperationFailure as ex:
            print(ex.value)
        except pyerrors.PyMongoError as ex:
            print(ex.value)
        print('remove: failed')
        return False
            
    def assign(self, prod1_name, prod2_name, times):
        """
        Assign a fixed times of the given pair of products with times purchased together
        """
        try:
            self._purchased.update({PROD1: prod1_name, PROD2: prod2_name},
                                   {'$set': {TIMES: times}},
                                   True
                                   )
            self._purchased.update({PROD1: prod2_name, PROD2: prod1_name},
                                   {'$set': {TIMES: times}},
                                   True
                                   )
            print('assign: succeeded')
            return True
        except pyerrors.OperationFailure as ex:
            print(ex.value)
        except pyerrors.PyMongoError as ex:
            print(ex.value)
        print('assign: failed')
        return False
    
    def how_many(self, prod):
        try:
            return self._purchased.find({PROD1: prod}).count()
        except pyerrors.OperationFailure as ex:
            print(ex.value)
        except pyerrors.PyMongoError as ex:
            print(ex.value)
        
            
    def recommend_next_product(self, prod_list):
        """
        Recommend the next best relevant product
        """
        scores = defaultdict(float)
        for prod in prod_list:
            for item in self._purchased.find({PROD1: prod}):
                if not item[PROD2] in prod_list:
                    scores[item[PROD2]] += math.log(item[TIMES])
        if len(scores) == 0:
            return None
        max_tuple = max(scores.items(), key = operator.itemgetter(1))
        return max_tuple[0]

    def get_times(self, prod1_name, prod2_name):
        """
        Get the # of times this pair has been purchased together
        """
        try:
            item = self._purchased.find_one({PROD1: prod1_name, PROD2: prod2_name})
            if item == None: return None
            else: return item[TIMES]
        except pyerrors.OperationFailure as ex:
            print(ex.value)
        except pyerrors.PyMongoError as ex:
            print(ex.value)

    def clear(self):
        try:
            self._purchased.remove()
            print('clear: succeeded')
            return True
        except pyerrors.OperationFailure as ex:
            print(ex.value)
        except pyerrors.PyMongoError as ex:
            print(ex.value)
        print('clear: failed')
        return False

#pm = ProductsManager()
#prod_list = []
#with open('../test/products.txt') as f:
#    for line in f:
#        prod_list.append(tuple(map(int, line.split())))
#    pm.insert_product_list(prod_list)
#print(pm.how_many(1))
#print(pm.recommend_next_product([1,2,3]))