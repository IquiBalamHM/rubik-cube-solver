
from rubikSolver import *
import cv2
import numpy as np

from scipy.optimize import linear_sum_assignment
cap=cv2.VideoCapture(0)
_,frame=cap.read()
height,width,_=frame.shape

#Here we define the cordinates of the small scuare based from the frames
square_size_factor=0.4#fraction of height of image that square occupies
square_x1=int((width-((square_size_factor)*height))/2)#coordinate calculation for square corners
square_x2=int((width+((square_size_factor)*height))/2)


square_y1=int(((1-square_size_factor)/2)*height)
square_y2=int(((1+square_size_factor)/2)*height)

cube_dimension=square_y2-square_y1#height and width of cube in pixels



cube=[]

counter= 1
#Print the order that you should follow for scanning    
print("g -> r -> b -> o -> y -> w")
print("F -> R -> B -> L -> U -> D")

def find_avg_hsv(img):#given the cropped image of cube face finds the hsv values of each cybie(or tile) and forms a 3d array of hsv values
    """Create a new user.
    Find the avg hsv colors from the small squares located in each subsquare.
    This calculation allows to only take into account subregions of the cube and that it does not have to be completely centered.
    """
    tile_dimension=int(cube_dimension/3)#as cube face has 9(3x3) tiles
    tile_factor=0.3#factor of area where colour will be found(tile roi)
    tile_roi_start=int(((1-tile_factor)/2)*tile_dimension)#pixels to start of bounding rectangle of tile roi
    tile_roi_end=int((tile_dimension*tile_factor)+tile_roi_start)#pixels to end of bounding rectangle of tile roi
    
    tile_roi=[]#list which will hold roi (in image form) of all individual tiles
    for j in range(3):
        row=[]
        for i in range(3):
            row.append(img[(j*tile_dimension)+tile_roi_start:(j*tile_dimension)+tile_roi_end,(i*tile_dimension)+tile_roi_start:(i*tile_dimension)+tile_roi_end])#roi finding math
            cv2.rectangle(img, ((i*tile_dimension)+tile_roi_start,(j*tile_dimension)+tile_roi_start), ((i*tile_dimension)+tile_roi_end,(j*tile_dimension)+tile_roi_end), (255,0,0), 1)#draws rectangle on each tile roi
        tile_roi.append(row)
    cv2.namedWindow("check")
    cv2.moveWindow("check", 40,30)
    cv2.imshow("check",img)
    hsv_avg=[]#list which will hold avg hsv value of each tile

    for row_iterable in tile_roi:
        row=[]
        bgr_row=[]
        for col_iterable in row_iterable:
            b_avg,g_avg,r_avg,_=np.uint8(cv2.mean(col_iterable))#averages bgr value in roi
            color=cv2.cvtColor(np.uint8([[[b_avg,g_avg,r_avg]]]),cv2.COLOR_BGR2LAB)#converts bgr value to corresponding hsv
            h_avg= color[0][0][0]
            s_avg= color[0][0][1]
            v_avg= color[0][0][2]
            row.append([h_avg,s_avg,v_avg])
        hsv_avg.append(row)
    
    return hsv_avg

while True:
    '''
    Continues loop that captures frames and calls the respective funtions to build the cube string represantion.
    Press space to save a new face and s when you are done to save it. To see the steps, close the matplotlib window.
    '''
    _,frame=cap.read()
    
    cv2.rectangle(frame, (square_x1, square_y1), (square_x2, square_y2), (0,255,120), 2)#cube should be placed within this square


    cv2.imshow("original",frame)
    k=cv2.waitKey(1) & 0xff
    if k==27:#ESC is pressed
        break
    elif k==32:#SPACE is pressed
        print("Image " + str(counter) + " Captured")
        cube_roi=frame[square_y1:square_y2,square_x1:square_x2]#image of cube only
        counter+=1
        cubeface=find_avg_hsv(cube_roi)
        cube.append(cubeface)
        
    elif k==ord('s'):
        cube_colors=find_colors(cube)
        plot_colors(cube_colors)
        solution6 = sol6(cube_colors)
        print("Using 6 motors: ")
        print(solution6)

    elif k==ord('r'):
        cube.pop()

#Safely release the video capture
cap.release()
cv2.destroyAllWindows()
