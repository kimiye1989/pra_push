#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 22:43:31 2018

@author: yeqiming
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


# read file #
f0 = 'coordinates.csv'
f1 = 'truckSol_test.csv'
f2 = 'droneSol_test.csv'

t = pd.read_csv(f1,header = None)
d = pd.read_csv(f2,header = None)
c = pd.read_csv(f0,header = None)

truck = np.array(t)
drone = np.array(d)
coord = np.array(c)
childlen = np.shape(truck)[1]


def LocatePosition(m):  
    
    row = np.shape(m)[0]
    
    x = []
    for i in range(row):
        tot = np.sum(m[i,:])
        if tot == 0:
            x.append(0)
        else:
            k = np.argwhere(m[i,:]==1)[0,0]+1
            x.append(k)
    for j in range(1,len(x)):
        if x[j] == 0:
            x[j] = x[j-1]
    return x

lis1 = LocatePosition(truck)
lis2 = LocatePosition(drone)
#print(lis1, lis2)



def SmallSteps(lis, childlen):
    list_of_group = zip(*(iter(lis),)*childlen)
    end_list = [list(i) for i in list_of_group]
    count = len(lis) % childlen
    end_list.append(lis[-count:]) if count !=0 else end_list
    return end_list

pathlis1 = SmallSteps(lis1,childlen)
pathlis2 = SmallSteps(lis2,childlen)

#print(pathlis1, pathlis2)


def PlotCoordinates(coo):
    list_x = []
    list_y = []
    
    os.chdir('/Users/yeqiming/Desktop/NetworkGraph 3/Output')
    
    plt.scatter([],[],color = 'red', label = 'Truck')
    plt.scatter([],[],color = 'green', label = 'Drone')
    plt.plot([],[],color = 'red', label = "Truck's Last Path")
    plt.plot([],[],color = 'green', label = "Drone's Last Path")
    
    for i in range(np.shape(coo)[0]):
        plt.scatter(coo[i][1], coo[i][2], s=30,color='grey')
        list_x.append(coo[i][1])
        list_y.append(coo[i][2])
    
    plt.xlim(min(list_x)-1, max(list_x)+1)
    plt.ylim(min(list_y)-1, max(list_y)+1)
        
    plt.xticks(np.arange(min(list_x), max(list_x)+1, 1.0))
    plt.yticks(np.arange(min(list_y), max(list_y)+1, 1.0))
    
    #plt.show()

def PlotPath(pas, coo):
    
    steplists = [[pas[0][0],pas[1][0]],[pas[0][1],pas[1][1]]]
    
    print(steplists)
    
    j = 1
    
    for steplist in steplists:
        
        colorrange1 = ['red', 'green']
        colorrange2 = ['darkgrey', 'lightgrey']
        
        for seq, i in zip(steplist, range(len(steplist))):
            
            listx = []
            listy = []
            
            currentcolor = colorrange1[i]
            postcolor = colorrange2[i]
    
            for xy in seq:
                
                listx.append(coo[xy-1][1])
                listy.append(coo[xy-1][2])
            
            #plot links             
            plt.plot(listx[:-1],listy[:-1],color= postcolor, linewidth=1)
            plt.plot([listx[-2],listx[-1]],[listy[-2],listy[-1]],color=currentcolor, linewidth=1)
            
            #plot nodes
            plt.scatter(listx[:-1], listy[:-1],color = 'black', s = 30)
            plt.scatter(listx[-1], listy[-1],color = currentcolor, s = 30)
            
        plt.legend(loc = 'upper right')
        plt.title('Step_%d'%(j))
        plt.savefig('Step_%d.png'%(j))
        
        j = j+1
        

PlotCoordinates(coord)

pathliss =[pathlis1, pathlis2]

PlotPath(pathliss, coord)




