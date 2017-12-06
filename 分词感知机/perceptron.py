# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 22:21:49 2017

@author: DellT5810
"""

with open('train.txt',encoding='utf8') as f:
    data = f.readlines()
    
print(data[0].strip('\n').split('  '))

