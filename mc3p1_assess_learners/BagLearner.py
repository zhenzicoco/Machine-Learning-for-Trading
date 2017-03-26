# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 14:35:25 2017

@author: yueyue
"""

import numpy as np

class BagLearner(object):
    
    def __init__(self,learner,bags = 20,boost = False,verbose = False,kwargs=None):
        self.learner=learner
        self.bags=bags
        self.boost=boost
        self.verbose=verbose
        learners = []
        for i in range(bags):
            learners.append(self.learner(**kwargs))
        self.learners=learners
        pass
    #GT account
    def author(self):
        return 'ywang3234'
    #build and save the model            
    def addEvidence(self,dataX,dataY):
        tree_list=list()
        for i in range(self.bags):
            random_index=np.random.randint(0,dataX.shape[0],dataX.shape[0])
            Xtrain=dataX[random_index]
            Ytrain=dataY[random_index]
            self.learners[i].addEvidence(Xtrain,Ytrain)
            tree_list.append(self.learners[i].result_tree)
            
        self.result_tree=tree_list
        return self.result_tree
    #query predictions     
    def query(self,Xtest):
        predict=np.zeros(Xtest.shape[0])
        for i in range(self.bags):
            predict=predict+self.learners[i].query(Xtest)
        
        self.predictions=predict/float(self.bags)
        if self.verbose==True:
            print self.predictions
        return self.predictions
        

        
        