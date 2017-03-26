# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 20:55:51 2017

@author: yueyue
"""

import numpy as np
import pandas as pd
class RTLearner(object):
    
    def __init__(self, leaf_size = 40, verbose = False):
        self.leaf_size=leaf_size
        self.verbose=verbose
        pass
    #GT account
    def author(self):
        return 'ywang3234'
    #build tree    
    def build_tree(self,dataX,dataY):
        if len(np.unique(np.array(dataY)))==1:
            return ['leaf',dataY[0],'NA','NA']
        elif dataX.shape[0]<= self.leaf_size:
            return ['leaf',dataY.mean(),'NA','NA']

        else:
            rand_feature=np.random.randint(0,dataX.shape[1])
            rand_rows=dataX[np.random.choice(dataX.shape[0], 2, replace=False), :]
            if rand_rows[0,rand_feature]==rand_rows[1,rand_feature]:
                return ['leaf',dataY.mean(),'NA','NA']
            
            else:
                SplitVal=float(rand_rows[:,rand_feature].sum())/2            
                lefttree=self.build_tree(dataX[dataX[:,rand_feature]<=SplitVal],
                                    dataY[dataX[:,rand_feature]<=SplitVal])
                righttree=self.build_tree(dataX[dataX[:,rand_feature]>SplitVal],
                                    dataY[dataX[:,rand_feature]>SplitVal]) 
                
                root=[rand_feature,SplitVal,1,len(lefttree)/4+1]
                return root+lefttree+righttree    
    #transform tree        
    def ParserResult(self, ls):
        tree=np.array(ls).reshape((len(ls)/4,4))
        rand_tree=pd.DataFrame(tree,columns=['Factor','SplitVal','left','right'])
        rand_tree['SplitVal']=rand_tree['SplitVal'].astype('float')
        return rand_tree
        
    # combine build tree and transform tree                  
    def addEvidence(self,dataX,dataY):
        res = self.build_tree(dataX,dataY)
        self.result_tree = self.ParserResult(res)    
        if self.verbose==True:
            print self.result_tree
        
    def query_one(self,row):    
        node=0
        while True:
            if self.result_tree['Factor'][node]!='leaf':
                split_factor=int(self.result_tree['Factor'][node])
                if row[split_factor]>self.result_tree['SplitVal'][node]:
                    node=node+int(self.result_tree['right'][node])
                else:
                    node=node+int(self.result_tree['left'][node])
            else:
                return self.result_tree['SplitVal'][node]
                break
    #query predictions     
    def query(self,Xtest):
        Xtest=pd.DataFrame(Xtest)
        return np.array(Xtest.apply(self.query_one,axis='columns'))
        
    
            
            
        
               
        

                            
                            
                            
                
        
        