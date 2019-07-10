import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime as time
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def generate_sudoku(mask_rate=0.7):
    while True:
        n = 9
        m = np.zeros((n, n), np.int)
        rg = np.arange(1, n + 1)
        m[0, :] = np.random.choice(rg, n, replace=False)
        try:
            for r in range(1, n):
                for c in range(n):
                    col_rest = np.setdiff1d(rg, m[:r, c])
                    row_rest = np.setdiff1d(rg, m[r, :c])
                    avb1 = np.intersect1d(col_rest, row_rest)
                    sub_r, sub_c = r//3, c//3
                    avb2 = np.setdiff1d(np.arange(0, n+1), m[sub_r*3:(sub_r+1)*3, sub_c*3:(sub_c+1)*3].ravel())
                    avb = np.intersect1d(avb1, avb2)
                    m[r, c] = np.random.choice(avb, size=1)
            break
        except ValueError:
            pass
    print("Answer:\n", m)
    mm = m.copy()
    mm[np.random.choice([True, False], size=m.shape, p=[mask_rate, 1 - mask_rate])] = 0
    print("\nMasked answer:\n", mm)
    np.save("puzzle", create_framework(mm))
    return mm

def create_framework(new_sudoku):
    return np.swapaxes(np.swapaxes(new_sudoku.reshape([3,3,3,3]),0,2),1,2)

def list_possibilities(framework):
    possiblelist=[]
    for i in range(1,10):
        if (i not in framework.flatten()):
            possiblelist.append(i)
    return possiblelist

def list_verticle_framework(framework):
    verticleposs=[]
    for i in range(3):
        for j in range(3):
            verticleposs.append(list_possibilities(framework[i,:,:,j]))
    return verticleposs

def list_horizontal_framework(framework):
    horizontalposs=[]
    for i in range(3):
        for j in range(3):
            #print (framework[:,i,j,:])
            horizontalposs.append(list_possibilities(framework[:,i,j,:]))
    return horizontalposs

def list_box_framework(framework):
    boxposs=[]
    for i in range(3):
        for j in range(3):
            #print (framework[i,j,:,:])
            boxposs.append(list_possibilities(framework[i,j,:,:]))
    return boxposs

def generate_positional_array(framework):
    framework_with_positional_element=np.zeros([3,3,3,3,4],dtype=int)
    for indexi,i in enumerate(framework):
        for indexj,j in enumerate(i):
            for indexk,k in enumerate(j):
                for indexl,l in enumerate(k):
                    #print(l,f'vrow is {3*indexi+indexl} hrow is {3*indexj+indexk} box is {3*indexi+indexj}')
                    framework_with_positional_element[indexi,indexj,indexk,indexl]=[l,3*indexi+indexl,3*indexj+indexk,3*indexi+indexj]
    return framework_with_positional_element

def solve(f,framework,tries,v_poss,h_poss,b_poss):
    count =0
    t0=time.now()
    remaining = 0
    remain_possible={"position":[],"possible_num":[]}
    while True:
        for ii,i in enumerate(f):
            for ij,j in enumerate(i):
                for ik,k in enumerate(j):
                    for il,l in enumerate(k):
                        #print(l)
                        if l[0]==0:
                            remaining_possibilities=np.intersect1d(np.intersect1d(v_poss[l[1]],h_poss[l[2]]),b_poss[l[3]])
                            #print(remaining_possibilities)
                            if len(remaining_possibilities)==1:
                                # print (f'replace index {ii}{ij}{ik}{il} with {remaining_possibilities[0]}')
                                framework[ii,ij,ik,il]=remaining_possibilities[0]
                                f[ii,ij,ik,il,0]=remaining_possibilities[0]
                            elif (len(remaining_possibilities)==0):
                                # print('sudoku is not possible')
                                return [2,None]
                            else:
                                remaining +=1
                                remain_possible["possible_num"].append(remaining_possibilities)
                                remain_possible["position"].append([ii,ij,ik,il])
        count +=1
        if remaining==0:print('sudoku is solved');return [0,remain_possible]
        if count>tries:return [1,remain_possible]
    print(f'sudoku completed after {(time.now()-t0).total_seconds()*1000} ms') if remaining ==0 else print (f'sudoku is still not completed after {(time.now()-t0).total_seconds()*1000} ms')



def plot(framework):
    ''' This function is used to plot the sudoku into a matplotlib chart'''
    data = []
    for i in framework:
        for j in i:
            data.append(pd.DataFrame(j))

    _, axn = plt.subplots(3, 3, sharex=True, sharey=True)

    for axis, dfi in zip(np.swapaxes(axn, 0, 1).flat, data):
        sns.heatmap(dfi, annot=True, ax=axis, cbar=False, cmap='Greys')
        axis.get_xaxis().set_visible(False)
        axis.get_yaxis().set_visible(False)
