# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 22:21:49 2017

@author: https://github.com/githubxiaowei
"""

import os

class ChSegment:
    
    def __init__(self):
        self.features = {}
        self.b = 0
    
    def parse(self,str): #导出训练数据的标签
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
    
    def train(self,lr=0.1):#训练
        train_x,train_y = [],[]
        with open('train.txt',encoding='utf8') as f:
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
                        self.features[f] += (2*gold_y-1)*lr
                        self.b += (2*gold_y-1)*lr
            #print('line:{} err:{}'.format(i,err/len(line)))
        return self
      
    def save(self,fpath):#储存特征对应的权值
        with open(fpath,'w',encoding='utf8') as f:
            f.write('b '+str(self.b)+'\n')
            for k in self.features:
                f.write(k+' '+str(self.features[k])+'\n')
                
    def load(self,fpath):#导入已经save的权值
        with open(fpath,encoding='utf8') as f:
            self.b = float(f.readline()[:-1].split(' ')[1])
            print(self.b)
            for line in f.readlines():
                l = line[:-1].split(' ')
                self.features[l[0]] = float(l[1])
        return self
            
    def feature(self,line,idx):#提取每一个字在句子中的特征
        ftr = []
        line = 'S'+line+'E'
        idx += 1
        ftr.append(line[idx])
        ftr.append(line[idx-1]+'_'+line[idx])
        ftr.append(line[idx]+'_'+line[idx+1])
        ftr.append(line[idx-1]+'_'+line[idx]+'_'+line[idx+1])
        #print(ftr)
        return ftr

    def output(self,feature):#每一次训练的模型输出{0,1}
        y = self.b
        for f in feature:
            if(f not in self.features):
                self.features[f] = 0.1
            y += self.features[f]
        return int(y>0)

    def predict(self,line):#对输入的句子分词
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
    
    def merge(self,cs,p1,p2):#合并两个模型的参数，p1、p2分别对应本模型和输入模型的比例
        p1 /=(p1+p2)
        p2 /=(p1+p2)
        self.b = p1*self.b + p2*cs.b
        for k in self.features:
            self.features[k] = p1*self.features[k] + p2*cs.features[k]
        return self


def average():#前50次训练模型的平均化
    cs = ChSegment().load('feature/feature_0')
    for i in range(1,50):
        print(i)
        cs.merge(ChSegment().load('feature/feature_'+str(i)),i,1)
        with open('test.txt',encoding='utf8') as fin:
            with open('average_answer/test.answer.'+str(i),'w',encoding='utf8') as fout:
                for line in fin.readlines():
                    fout.write(cs.predict(line[:-1])+'\n')
        '''
        os.system('perl score gold/vocab.txt gold/test.answer.txt average_answer/test.answer.'+str(i)+' > score.utf8')
        with open('score.utf8',encoding='utf8') as f:
            lines = f.readlines()
        l = lines[-1].split('\t')
        print('recall:{},acc:{},Fscore:{}'.format(l[-6],l[-5],l[-4]))
        '''

def simple():#前50次训练的结果
    cs = ChSegment()
    for i in range(50):
        print(i)
        cs.train()
        #cs.save('feature/feature_'+str(i))
        with open('test.txt',encoding='utf8') as fin:
            with open('answer/test.answer.'+str(i),'w',encoding='utf8') as fout:
                for line in fin.readlines():
                    fout.write(cs.predict(line[:-1])+'\n')
        '''
        os.system('perl score gold/vocab.txt gold/test.answer.txt answer/test.answer.'+str(i)+' > score.utf8')
        with open('score.utf8',encoding='utf8') as f:
            lines = f.readlines()
        l = lines[-1].split('\t')
        print('recall:{},acc:{},Fscore:{}'.format(l[-6],l[-5],l[-4]))
        '''


if(__name__ == '__main__'):
    #如需直接测评，除去多行注释
    simple() 
    #average()