import os

import torch
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split

class FGD():
    def __init__(self,dir_root,test_ratio=0.3):
        self.dir_root = dir_root
        self.test_ratio = test_ratio
        self.load()



    def load(self):
        dir_root = self.dir_root
        test_ratio = self.test_ratio
        # Read 
        self.df_file = pd.DataFrame(columns={'file'})

        df_same = pd.DataFrame({'file':\
            [ dir_root+'/same/' + x for x in os.listdir(dir_root + '/same')]\
            ,'label':1})
        df_diff = pd.DataFrame({'file':\
            [ dir_root+'/diff/' + x for x in os.listdir(dir_root + '/diff')]\
            ,'label':0})

        # adjust distribution

        ratio = len(df_same)/len(df_diff)
        if ratio > 1 :
            ratio = 1
        print('ratio : ' + str(ratio))
        df_diff = df_diff.sample(frac = ratio)

        self.df_file = self.df_file.append(df_same,ignore_index=True,sort=True)
        self.df_file = self.df_file.append(df_diff,ignore_index=True,sort=True)

        print('label 0 : ' + str(len(self.df_file[self.df_file['label'] == 0])))
        print('label 1 : ' + str(len(self.df_file[self.df_file['label'] == 1])))

        # separte
        train, test = train_test_split(self.df_file, test_size=test_ratio)
        self.train = train
        self.test = test

        # Build
        self.trainset = FGD_train(train)
        self.testset = FGD_test(test)



        
    
    def get(self):
        return self.trainset, self.testset

class FGD_train(torch.utils.data.Dataset):
    def __init__(self,df):
        self.pd_train = df
        self.length = len(self.pd_train)
        return
    
    def __len__(self):
        return self.length

    def __getitem__(self,idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
        path = self.pd_train.iloc[idx]['file']
        values = torch.Tensor(np.load(path))
        label = int( self.pd_train.iloc[idx]['label'])

        sample = (values,label)

        return sample

class FGD_test(torch.utils.data.Dataset):
    def __init__(self,df):
        self.pd_test = df
        self.length = len(self.pd_test)
        return
    
    def __len__(self):
        return self.length

    def __getitem__(self,idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
        path = self.pd_test.iloc[idx]['file']
        values = torch.Tensor(np.load(path))
        label = int( self.pd_test.iloc[idx]['label'])

        sample = (values,label)

        return sample

