import numpy as np
import math
import copy
from sklearn.decomposition import PCA

import matplotlib.pyplot as plt

from bayes_opt import BayesianOptimization

import pywt.data
import csv,math,xlwt
import xlsxwriter
import xlrd
import math

import xlrd,xlsxwriter



def import_excel_matrix(path):
    table = xlrd.open_workbook(path).sheets()[0]  # 获取第一个sheet表
    row = table.nrows  # 行数
    data_matrix = []
    for i in range(row):  # 对列进行遍历
        data_matrix.append(table.row_values(i))
    return data_matrix


def save(data,path):
    f = xlsxwriter.Workbook(path)  # 创建工作簿
    sheet1 = f.add_worksheet('sheet1')  # 创建sheet
    l = len(data[0])
    h = len(data)  # h为行数，l为列数
    for i in range(h):
        for j in range(l):
            sheet1.write(i, j, data[i][j])
    f.close()


path_v = r'C:\Users\liuju\Documents\MATLAB\MIT_HIT\对比\五种类别\train\归一化\V.xlsx'
path_s = r'C:\Users\liuju\Documents\MATLAB\MIT_HIT\对比\五种类别\train\归一化\S.xlsx'
path_n = r'C:\Users\liuju\Documents\MATLAB\MIT_HIT\对比\五种类别\train\归一化\N.xlsx'
path_u = r'C:\Users\liuju\Documents\MATLAB\MIT_HIT\对比\五种类别\train\归一化\U.xlsx'
path_f = r'C:\Users\liuju\Documents\MATLAB\MIT_HIT\对比\五种类别\train\归一化\F.xlsx'


path_ts = r'C:\Users\liuju\Documents\MATLAB\MIT_HIT\对比\五种类别\test\归一化\S.xlsx'

data_v = import_excel_matrix(path_v)
data_s = import_excel_matrix(path_s)
data_n = import_excel_matrix(path_n)
data_u = import_excel_matrix(path_u)
data_f = import_excel_matrix(path_f)

data_ts = import_excel_matrix(path_ts)

def get_num(data,s,r = 0.03):
    data = np.mat(data)    
    [m,n] = data.shape
    lev = (m/(1/(2*r)))
    
    out = []
    for i in range(n):
        num_down = s[i] - r
        num_up = s[i] + r

        dia = [num_down,num_up]
        if num_down <= 0 :
            num_down = 0
        if num_up >= 1:
            num_up = 1
        if num_down == 0:
            dia = [0,r]
        if num_up == 1:
            dia = [1-2*r,1]
        
        tem_m = data[:,i]
        tem_m = np.array(tem_m)
        new_list = tem_m[(dia[0] <= tem_m) & (tem_m <= dia[1])]
        num = len(new_list)

        out.append(num)
    for t in range(len(out)):
        # if out[t] >= lev:
        #     out[t] = 1
        # else:
        #     out[t] = 0     
        out[t] = out[t]/lev  
    return sum(out)
# s_v = data_v[0]

def start_train(r):
    rate = 0
    data_sect = data_ts
    for i in range(len(data_sect)):
        s_s = data_sect[i]
        out_1 = get_num(data_s,s_s,r)
        out_2 = get_num(data_v,s_s,r)
        out_3 = get_num(data_n,s_s,r)
        out_4 = get_num(data_u,s_s,r)
        out_5 = get_num(data_f,s_s,r)

        if out_1 == max([out_1,out_2,out_3,out_4,out_5]):
            rate = rate + 1

    return rate/len(data_sect)



rf_bo = BayesianOptimization(start_train,{'r':(0.001,0.4999)})
rf_bo.maximize()
