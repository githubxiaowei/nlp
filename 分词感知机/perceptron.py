# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 22:21:49 2017

@author: https://github.com/githubxiaowei
"""

class ChSegment:
    
    def __init__(self):
        self.features = {}
        self.b = 0
    
    def parse(self,str):
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
    
    def train(self):
        train_x,train_y = [],[]
        with open('train.bak',encoding='utf8') as f:
                for line in f.readlines():
                    train_x.append(line[:-1].replace('  ',''))
                    train_y.append(self.parse(line[:-1]))
                    
        for i,line in enumerate(train_x):
            err = 0
            for j in range(len(line)):
                ftr = self.feature(line,j)
                gold_y = int(train_y[i][j])
                if(not gold_y==self.output(ftr)):
                    err += 1
                    for f in ftr:
                        self.features[f] += (2*gold_y-1)*0.2
            print('line:{} err:{}'.format(i,err/len(line)))
        return self
      
    def save(self,fpath):
        with open(fpath,'w',encoding='utf8') as f:
            for k in self.features:
                f.write(k+' '+str(self.features[k])+'\n')
                
    def load(self,fpath):
        with open(fpath,encoding='utf8') as f:
            for line in f.readlines():
                l = line[:-1].split(' ')
                self.features[l[0]] = float(l[1])
        return self
            
    def feature(self,line,idx):
        ftr = []
        line = 'S'+line+'E'
        idx += 1
        ftr.append(line[idx])
        ftr.append(line[idx-1]+'_'+line[idx])
        ftr.append(line[idx]+'_'+line[idx+1])
        ftr.append(line[idx-1]+'_'+line[idx]+'_'+line[idx+1])
        return ftr

    def output(self,feature):
        y = self.b
        for f in feature:
            if(f not in self.features):
                self.features[f] = 0.1
            y += self.features[f]
        return int(y>0)

    def predict(self,line):
        y = ''
        for j in range(len(line)):
            ftr = self.feature(line,j)
            y+=str(self.output(ftr))
        seg = ''
        for idx,ch in enumerate(line):
            if(y[idx] == '1'):
                seg += '  '
            seg += ch
        return seg

if(__name__ == '__main__'):
    cs = ChSegment().load('features')
    with open('test.txt',encoding='utf8') as fin:
        with open('text.answer.bak','w',encoding='utf8') as fout:
            for line in fin.readlines():
                fout.write(cs.predict(line[:-1])+'\n')
    
    

