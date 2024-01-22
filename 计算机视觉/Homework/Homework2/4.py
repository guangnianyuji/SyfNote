import numpy as np
import cv2
from tqdm import tqdm
u_image=cv2.imread('1.jpg')#undistorted image

#你想生成的图片像素
m=1800  # y
n=2400  # x

h=300
#p_bw=np.array([[h/m,0,-h*n/m/2],[0,-h/m,h/2],[0,0,1]])
p_bw=np.array([[h/m,0,-h*n/m/6],[0,h/m,-h/6],[0,0,1]])

#x_u=[[1257,815],[2337,871],[1274,1993],[2369,1936]]#用windows画图软件打开图片，选四个点，记录坐标在此
x_u=[[1562,1032],[2473,1052],[1560,1666],[2779,1613]]
x_w=[[0,0],[88,0],[0,88],[88,88]]#真正的长度，以mm为单位

A=np.zeros((8,8))
b=np.zeros((8,1))

for i in range(4):
    A[2*i][0]=x_w[i][0]
    A[2*i][1]=x_w[i][1]
    A[2*i][2]=1
    
    A[2*i][6]=-x_w[i][0]*x_u[i][0]
    A[2*i][7]=-x_w[i][1]*x_u[i][0]
    
    A[2*i+1][3]=x_w[i][0]
    A[2*i+1][4]=x_w[i][1]
    A[2*i+1][5]=1
    
    A[2*i+1][6]=-x_w[i][0]*x_u[i][1]
    A[2*i+1][7]=-x_w[i][1]*x_u[i][1]
    
    b[2*i][0]=x_u[i][0]
    b[2*i+1][0]=x_u[i][1]

h_=np.linalg.inv(A.T@A)@A.T@b

p_wu=np.zeros((3,3))

for i in range(3):
    for j in range(3):
        if(i==2 and j==2):
            p_wu[i][j]=1
            break
        p_wu[i][j]=h_[i*3+j]
o1=np.zeros((m,n,3))      
out_image=np.zeros((m,n,3))

u_image_shape=u_image.shape
print(u_image_shape)#h w = y x 
for j in tqdm(range(m)): #y
    for i in range(n): # x
        cor=p_bw@np.array([i,j,1]) # x y
        cor=cor/cor[2]
        xx=int(cor[0])
        yy=int(cor[1])
        if(yy>=0 and yy<u_image_shape[0] and xx>=0 and xx<u_image_shape[1]):
             
            o1[j][i]=u_image[yy][xx]
        cor=p_wu@cor
        cor=cor/cor[2]
        #print(cor)
        xx=int(cor[0])
        yy=int(cor[1])
        if(yy>=0 and yy<u_image_shape[0] and xx>=0 and xx<u_image_shape[1]):
             
            out_image[j][i]=u_image[yy][xx]
#cv2.imwrite("o.png",o1)
cv2.imwrite("bv.png",out_image)
        

 