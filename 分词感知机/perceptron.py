# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 22:21:49 2017

@author: https://github.com/githubxiaowei
"""

def parse(str):
    target = ''
    flag = 0
    for c in str:
        if(c==' '):
            flag += 1
            continue
        if(flag==2):
            target += '1'
            flag = 0
        else:
            target += '0'
    return target

train_x,train_y = [],[]
with open('train.txt',encoding='utf8') as f:  
    for line in f.readlines():
        train_x.append(line[:-1].replace('  ',''))
        train_y.append(parse(line[:-1]))





