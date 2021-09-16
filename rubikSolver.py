import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from sklearn.cluster import KMeans
from scipy.optimize import linear_sum_assignment

import kociemba




def replace_values(arr,replace,replacement):
    for i in range(len(arr)):
        if arr[i]==replace:
            arr[i]=replacement
    return arr


def sol(input1):
    input2=[[[]],[[]],[[]],[[]],[[]],[[]]]

    for i in range(6):
        if(input1[i][1][1]=='w'):
            input2[0]=input1[i]
            break

    for i in range(6):
        if(input1[i][1][1]=='r'):
            input2[1]=input1[i]
            break
    
    for i in range(6):
        if(input1[i][1][1]=='g'):
            input2[2]=input1[i]
            break

    for i in range(6):
        if(input1[i][1][1]=='y'):
            input2[3]=input1[i]
            break

    for i in range(6):
        if(input1[i][1][1]=='o'):
            input2[4]=input1[i]
            break

    for i in range(6):
        if(input1[i][1][1]=='b'):
            input2[5]=input1[i]
            break
    
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
    
    a = kociemba.solve(b)
    #print(a)
    return a

def cleansolution(solution):
    cleanedsolution=""
    prev=solution[0]
    for current in solution[1:]:
        if current=="'":
            cleanedsolution+=prev.lower()
        elif current=="2":
            cleanedsolution+=prev
            cleanedsolution+=prev
        else:
            cleanedsolution+=prev
        prev=current
    cleanedsolution+=solution[len(solution)-1]
    cleanedsolution = cleanedsolution.replace("'", "")
    cleanedsolution = cleanedsolution.replace("2", "")
    cleanedsolution = cleanedsolution.replace(" ", "")
    
    return cleanedsolution

def create_cost_matrix(mat1,mat2):
    res = np.eye(6)
    for r in range(6):
        for c in range(6):
            res[r][c] = np.linalg.norm(mat1[r]-mat2[c])
    #dist = np.linalg.norm(mat1-mat2)
    return res

def min_cost(mat1,mat2):
    cost_matrix = create_cost_matrix(mat1,mat2)

    #print(cost_matrix)
    row_ind, col_ind = linear_sum_assignment(cost_matrix=cost_matrix,
                                             maximize=False)

    minimum_cost = cost_matrix[row_ind, col_ind].sum()
    return list(zip(row_ind, col_ind))
def find_colors(cube):
    cube=np.array(cube).reshape(-1,3)
    kmeans=KMeans(n_clusters=6,random_state=0,n_init=1,max_iter=200)
    kmeans.fit(cube)
    preds=kmeans.labels_
    preds=preds.tolist()
    
    unique, counts = np.unique(preds, return_counts=True)


    #print(np.asarray((unique, counts)).T)
    if(counts.tolist()!=[9]*6):
        print("COLOR SCAN FAILED")
    else:
        print("SCAN SUCCESFULL")

    copypreds = np.copy(preds)
    copypreds2 = np.copy(copypreds)
    copypreds2=np.where(copypreds==copypreds[4],"g",copypreds2)
    copypreds2=np.where(copypreds==copypreds[4+9],"r",copypreds2)
    copypreds2=np.where(copypreds==copypreds[4+9*2],"b",copypreds2)
    copypreds2=np.where(copypreds==copypreds[4+9*3],"o",copypreds2)
    copypreds2=np.where(copypreds==copypreds[4+9*4],"w",copypreds2)
    copypreds2=np.where(copypreds==copypreds[4+9*5],"y",copypreds2)
    copypreds2=np.array(copypreds2).reshape(6,3,3)
    #print(copypreds2)
    return copypreds2



def plot_colors(colors):
    colors=np.where(colors=="r","0",colors)
    colors=np.where(colors=="b","1",colors)
    colors=np.where(colors=="o","2",colors)
    colors=np.where(colors=="g","3",colors)
    colors=np.where(colors=="w","5",colors) #4
    colors=np.where(colors=="y","4",colors) #5
    colors=colors.astype(int)
    #print(colors)
    N=12
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

    plt.show()