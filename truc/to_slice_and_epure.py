import os
from PIL import Image as img
import numpy as np

def switch(newData,switch_mat):
    Data=newData.copy()
    col=Data[0].copy()
    for a in range(len(Data)):
        for b in range(len(Data[0])):
            if (newData[a,b]==col)[:3].all():
                Data[a,b]=switch_mat[1]
    return Data

image=img.open('Android_18_SpriteSheet.png')
rgba=image.convert('RGBA')
ar=np.array(rgba)
dark=ar[0,0]
w=0
while (ar[w,10]==dark).all():
    w+=1
light=ar[w,10]
x,y,_=ar.shape
i,j=0,0
k=0

switch_mat=np.array([light,np.array([0,0,0,0])])

while i+j<x+y:
    k2=0
    i_min,j_min=i,j
    i_max,j_max=i+1,j+1
    while i_min<i_max and i_max<x and j_min<j_max and j_max<y:
        while i_min<x and j_min<y and (ar[i_min,j_min]==dark).all():
            i_min+=1
            if i_min>=x:
                i_min=i_max
                j_min+=1
        i_max,j_max=i_min,j_min
        while i_max<x and j_max<y and not ((ar[i_max,j_max]==dark).all()):
            i_max+=1
            if i_max>=x:
                i_max=i_min+1
                j_max+=1
        while j_min<y and j_max<y:
            j_max=j_min+1
            while i_min<x and j_max<y and not ((ar[i_min,j_max]==dark).all()):
                j_max+=1

            if i_min<x and i_max<x and j_min<y and j_max<y:
                if not os.path.exists(str(k)):
                    os.mkdir(str(k))
                if not os.path.exists(str(k)+'/'+str(k2)):
                    newData=ar[i_min:i_max,j_min:j_max]
                    Data=switch(newData,switch_mat)
                    frame=img.fromarray(Data)
                    frame.save(str(k)+'/'+str(k2)+'.png')
            k2+=1
            j_min=j_max
            while i_min<x and j_min<y and ((ar[i_min,j_min]==dark).all()):
                j_min+=1
    k+=1
    i=i_max
    
