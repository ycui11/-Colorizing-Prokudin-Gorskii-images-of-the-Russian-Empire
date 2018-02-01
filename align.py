import matplotlib.pyplot as plt
from PIL import Image, ImageChops
import numpy as np
from scipy.misc import imresize
import tifffile
imname='00351v.jpg'
img=Image.open(imname)
img=np.asarray(img)
print(img.shape)
plt.imshow(img)


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

w,h=img.shape
height=int(w/3)
blue=img[0:height,:]
green=img[height:2*height,:]
red=img[2*height:3*height,:]
plt.figure()
plt.imshow(blue)
plt.figure()
plt.imshow(green)
plt.figure()
plt.imshow(red)
def ncc(a,b):
    a=a-a.mean(axis=0)
    b=b-b.mean(axis=0)
    return np.sum(((a/np.linalg.norm(a)) * (b/np.linalg.norm(b))))
def nccAlign(a, b, t):
    min_ncc = -1
    ivalue=np.linspace(-t,t,2*t,dtype=int)
    jvalue=np.linspace(-t,t,2*t,dtype=int)
    for i in ivalue:
        for j in jvalue:
            nccDiff = ncc(a,np.roll(b,[i,j],axis=(0,1)))
            if nccDiff > min_ncc:
                min_ncc = nccDiff
                output = [i,j]
    return output
alignGtoB = nccAlign(blue,green,20)
alignRtoB = nccAlign(blue,red,20)
print(alignGtoB, alignRtoB)
g=np.roll(green,alignGtoB,axis=(0,1))
r=np.roll(red,alignRtoB,axis=(0,1))
coloured = (np.dstack((r,g,blue))).astype(np.uint8)
coloured=coloured[int(coloured.shape[0]*0.05):int(coloured.shape[0]-coloured.shape[0]*0.05),int(coloured.shape[1]*0.05):int(coloured.shape[1]-coloured.shape[1]*0.05)]
coloured = Image.fromarray(coloured)
coloured.save('000351v.jpg')
plt.figure()
plt.imshow(coloured)