import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from sklearn.cluster import KMeans
from scipy.optimize import linear_sum_assignment

import kociemba




def replace_values(arr,replace,replacement):
    '''
    Replace values in an array given with the provided replacement value, works for single characters.
    '''
    for i in range(len(arr)):
        if arr[i]==replace:
            arr[i]=replacement
    return arr


def sol6(input1):
    '''
    Return the actual solution for a given string. 
    First converts the input from a colored string to a cube string that is accepted by the kociemba algorithm. 
    '''
    input2=[[[]],[[]],[[]],[[]],[[]],[[]]]#Initialize the array
    for i in range(6): 
        if(input1[i][1][1]=='w'): #Search for the first appearances of w
            input2[0]=input1[i]
            break

    for i in range(6):
        if(input1[i][1][1]=='r'): #Search for appearances of r
            input2[1]=input1[i]
            break
    
    for i in range(6):
        if(input1[i][1][1]=='g'): #search for appearances of g 
            input2[2]=input1[i]
            break

    for i in range(6):
        if(input1[i][1][1]=='y'): #search for appearances of y
            input2[3]=input1[i]
            break

    for i in range(6):
        if(input1[i][1][1]=='o'): #search for appearances of o
            input2[4]=input1[i]
            break

    for i in range(6):
        if(input1[i][1][1]=='b'): #search for appearances of y
            input2[5]=input1[i]
            break
    
    ##Change those appearances to the needed representation as U, D, R, L, F, B
    for i in range(6):
        for j in range(3):
            for k in range(3):
                if (input2[i][j][k]=='w'):
                    input2[i][j][k]='U'
                elif (input2[i][j][k]=='y'):
                    input2[i][j][k]='D'
                elif (input2[i][j][k]=='r'):
                	input2[i][j][k]='R'
                elif (input2[i][j][k]=='o'):
                	input2[i][j][k]='L'
                elif (input2[i][j][k]=='g'):
                	input2[i][j][k]='F'
                elif(input2[i][j][k]=='b'):
                	input2[i][j][k]='B'
    b=''
    for i in range(6):
    	for j in range(3):
    		for k in range(3):
    			b+=input2[i][j][k]

    #Call kociemba algorithm
    a = kociemba.solve(b)
    #print(a)
    return a

def find_colors(cube):
    '''
    Find the groups of colors in the cube using Kmeans clustering, provided by sklearn.
    '''
    cube=np.array(cube).reshape(-1,3)#Reshape the cube to a single line
    kmeans=KMeans(n_clusters=6,random_state=0,n_init=1,max_iter=200) #Do the grouping
    kmeans.fit(cube) #Fit the model
    preds=kmeans.labels_
    preds=preds.tolist() #Conver prediction to lists
    
    unique, counts = np.unique(preds, return_counts=True) #Find unique elements

    #If we can achieve the 6 different groups each one with 9 colors, then it's a succesful scan
    if(counts.tolist()!=[9]*6):
        print("COLOR SCAN FAILED")
    else:
        print("SCAN SUCCESFULL")

    #Use the predictions and change the labels to colors.
    copypreds = np.copy(preds)
    copypreds2 = np.copy(copypreds)
    copypreds2=np.where(copypreds==copypreds[4],"g",copypreds2)
    copypreds2=np.where(copypreds==copypreds[4+9],"r",copypreds2)
    copypreds2=np.where(copypreds==copypreds[4+9*2],"b",copypreds2)
    copypreds2=np.where(copypreds==copypreds[4+9*3],"o",copypreds2)
    copypreds2=np.where(copypreds==copypreds[4+9*4],"w",copypreds2)
    copypreds2=np.where(copypreds==copypreds[4+9*5],"y",copypreds2)
    copypreds2=np.array(copypreds2).reshape(6,3,3)

    return copypreds2



def plot_colors(colors):
    '''
    Used for visual purposes, print the flat version of the cube using Matplotlib.     
    '''
    #Crate labels for each colors
    colors=np.where(colors=="r","0",colors) #0
    colors=np.where(colors=="b","1",colors) #1
    colors=np.where(colors=="o","2",colors) #2
    colors=np.where(colors=="g","3",colors) #3
    colors=np.where(colors=="w","5",colors) #4
    colors=np.where(colors=="y","4",colors) #5
    colors=colors.astype(int)

    N=12
    #Color the squares
    data = np.ones((N,N)) * np.nan
    data[3:6,3:6]=colors[0]
    data[3:6,6:9]=colors[1]
    data[3:6,9:12]=colors[2]
    data[3:6,0:3]=colors[3]
    data[0:3,3:6]=colors[4]
    data[6:9,3:6]=colors[5]
    # make a figure + axes
    fig, ax = plt.subplots(1, 1, tight_layout=True)
    # make color map
    my_cmap = matplotlib.colors.ListedColormap(['r', 'b', 'darkorange','g','w','yellow'])
    # set the 'bad' values (nan) to be white and transparent
    my_cmap.set_bad(color='k')
    # draw the grid
    for x in range(N + 1):
        if(x%3==0):
            lw=5
        else:
            lw=2
        ax.axhline(x, lw=lw, color='k', zorder=5)
        ax.axvline(x, lw=lw, color='k', zorder=5)
    # draw the boxes
    ax.imshow(data, interpolation='none', cmap=my_cmap, extent=[0, N, 0, N], zorder=0)
    # turn off the axis labels
    ax.axis('off')
    # show
    plt.show()