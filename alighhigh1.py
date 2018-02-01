import matplotlib.pyplot as plt
from PIL import Image, ImageChops
import numpy as np
from scipy.misc import imresize

imname='01861a.tif'
img=Image.open(imname)
img=np.asarray(img)
w,h=img.shape
print(w,h)
plt.figure()
plt.imshow(img)

w,h=img.shape
print(w,h)
img=img[int(w*0.01):int(w-w*0.02),int(h*0.05):int(h-h*0.05)]
w,h=img.shape
print(w,h)
plt.imshow(img)
print(img.shape)
image_stack=[]
for i in range(1,5):
    scale=1/(i**2)
    image=imresize(img,scale)
    image_stack.append(image)
image_stack.reverse()
for im in image_stack:
    print (im.shape)
def ncc(a,b):
    a=a-a.mean(axis=0)
    b=b-b.mean(axis=0)
    return np.sum(((a/np.linalg.norm(a)) * (b/np.linalg.norm(b))))
def nccAlign(a, b, x,y,t):
    min_ncc = -1
    ivalue=np.linspace(-t+x,t+x,2*t,dtype=int)
    jvalue=np.linspace(-t+y,t+y,2*t,dtype=int)
    for i in ivalue:
        for j in jvalue:
            nccDiff = ncc(a,np.roll(b,[i,j],axis=(0,1)))
            if nccDiff > min_ncc:
                min_ncc = nccDiff
                output = [i,j]
    print(output)
    return output

for i in range(4):
    img=image_stack[i]
    print(img.shape)
    w,h=img.shape
    height=int(w/3)
    blue=img[0:height,:]
    green=img[height:2*height,:]
    red=img[2*height:3*height,:]
    x_gtob,y_gtob=0,0
    x_rtob,y_rtob=0,0
    alignGtoB = nccAlign(blue,green,x_gtob,y_gtob,20)
    alignRtoB = nccAlign(blue,red,x_rtob,y_rtob,20)
    x_gtob,y_gtob=alignGtoB[0]*2,alignGtoB[1]*2
    x_rtob,y_rtob=alignRtoB[0]*2,alignRtoB[1]*2

g=np.roll(green,[x_gtob,y_gtob],axis=(0,1))
r=np.roll(red,[x_rtob,y_rtob],axis=(0,1))
coloured = (np.dstack((r,g,blue))).astype(np.uint8)
coloured=coloured[int(coloured.shape[0]*0.05):int(coloured.shape[0]-coloured.shape[0]*0.05),int(coloured.shape[1]*0.05):int(coloured.shape[1]-coloured.shape[1]*0.05)]
coloured = Image.fromarray(coloured)
plt.figure()
plt.imshow(coloured)
