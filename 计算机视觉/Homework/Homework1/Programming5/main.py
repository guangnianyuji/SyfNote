import random
import numpy as np
import matplotlib.pyplot as plt
import cv2
from tqdm import tqdm
 
def homogeneousLinearSquares(A):
    U,S,V=np.linalg.svd(A.T@A,full_matrices=False)
    ans=V[-1].T
    ans=ans/ans[0] 
    return ans
  
            


def RANSAC(mpl,mpr,k,t,d,n=4):

    #compute H@mpr=mpl
    bestFit=None
    bestErr=0x7fffffffff

    for i in tqdm(range(k)):
     
        indices = random.sample(range(len(mpl)), n)
        
        A=np.zeros((8,9))
        
        for j in range(n):
            
            index=indices[j]
            # print(mpl[index])
            # print(mpr[index])
            # input('enter')
            row_num=j*2
            
            A[ row_num][0]=mpr[index][0]
            A[ row_num][1]=mpr[index][1]
            A[ row_num][2]=1
            A[row_num][6]=-mpr[index][0]*mpl[index][0]
            A[row_num][7]=-mpr[index][1]*mpl[index][0]
            A[row_num][8]=-mpl[index][0]
            
            A[row_num+1][3]=mpr[index][0]
            A[row_num+1][4]=mpr[index][1]
            A[row_num+1][5]=1
            A[row_num+1][6]=-mpr[index][0]*mpl[index][1]
            A[row_num+1][7]=-mpr[index][1]*mpl[index][1]
            A[row_num+1][8]=-mpl[index][1]
        #print("A",A)
        model=homogeneousLinearSquares(A)
        #print(model)
        H=np.zeros((3,3))
        for _ in range(model.shape[0]):
            H[int(_/3)][_%3]=model[_]
        #print("H",H)    

        alsoInliers=[]
        #input("enter")
        for j in range(len(mpl)):
            
            l_point=mpl[j]
            r_point=mpr[j]
            c_applied_r_point=H@np.array([[r_point[0]],[r_point[1]],[1]])
            applied_r_point=np.array([c_applied_r_point[0]/c_applied_r_point[2],
                                      c_applied_r_point[1]/c_applied_r_point[2]]) 
            distance=(l_point[0]-applied_r_point[0])**2+(l_point[1]-applied_r_point[1])**2
            # if j in indices:
            #     print("l",l_point)
            #     print("r",r_point)
            #     print("ar",applied_r_point)
            #     print("dis",distance)
            # #     input('enter')
            # print("dis",distance)
            # input('enter')
            if distance<t:
                alsoInliers.append(j)
        
        inlierNum=len(alsoInliers)
        #print(inlierNum)
        #input('enter')
        if inlierNum>=d:
           # print("yes") 
            A=np.zeros((2*inlierNum,9))
            for _ in range(inlierNum):
                index=alsoInliers[_]
                row_num=_*2
                A[row_num][0]=mpr[index][0]
                A[row_num][1]=mpr[index][1]
                A[row_num][2]=1
                A[row_num][6]=-mpr[index][0]*mpl[index][0]
                A[row_num][7]=-mpr[index][1]*mpl[index][0]
                A[row_num][8]=-mpl[index][0]
                
                A[row_num+1][3]=mpr[index][0]
                A[row_num+1][4]=mpr[index][1]
                A[row_num+1][5]=1
                A[row_num+1][6]=-mpr[index][0]*mpl[index][1]
                A[row_num+1][7]=-mpr[index][1]*mpl[index][1]
                A[row_num+1][8]=-mpl[index][1]
                
            betterModel= homogeneousLinearSquares(A)
            betterH=np.zeros((3,3))
            for _ in range(model.shape[0]):
                betterH[int(_/3)][_%3]=betterModel[_]
            thisErr=0.0
            for j in range(len(mpl)):
                l_point=mpl[j]
                r_point=mpr[j]
                
                c_applied_r_point=H@np.array([[r_point[0]],[r_point[1]],[1]])
                applied_r_point=np.array([c_applied_r_point[0]/c_applied_r_point[2],
                                        c_applied_r_point[1]/c_applied_r_point[2]]) 
                distance=(l_point[0]-applied_r_point[0])**2+(l_point[1]-applied_r_point[1])**2

                thisErr+=distance
            
            
            if thisErr<bestErr:
                bestFit=betterH
                bestErr=thisErr
    return bestFit   
                
            

def siftFeatures(image):
    
    grayimage=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    sift = cv2.SIFT_create(nfeatures=500)
    keypoints, descriptors = sift.detectAndCompute(image, None)
    return keypoints,descriptors 

def keypointMatch(kpsl,dcpsl,kpsr,dcpsr):
    # create Brute-Force match object
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)

    # match
    matches = bf.match(dcpsl,dcpsr)

    # sort by distance
    matches = sorted(matches, key=lambda x: x.distance)

    # distract coordinates
    mpl = [kpsl[m.queryIdx].pt for m in matches]
    mpr = [kpsr[m.trainIdx].pt for m in matches]
    return mpl,mpr,matches   

def main():
    
    imgl=cv2.imread('image/l.jpg')
    imgr=cv2.imread('image/r.jpg')

    kpsl, dcpsl=siftFeatures(imgl)
    imgl_with_kps=cv2.drawKeypoints(imgl,  kpsl,None)
    cv2.imwrite("image/imgl_with_kps.jpg",imgl_with_kps)
 
    kpsr, dcpsr=siftFeatures(imgr)
    imgr_with_kps=cv2.drawKeypoints(imgr,  kpsr,None)
    cv2.imwrite("image/imgr_with_kps.jpg",imgr_with_kps)
    
    mpl,mpr,matches=keypointMatch(kpsl,dcpsl,kpsr,dcpsr)
    match_image = cv2.drawMatches(imgl, kpsl, imgr, kpsr, matches, None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    cv2.imwrite('image/match_image.jpg',match_image)
 
    if(len(mpl)<4):
        print("match failure")
        exit(0)
    
    H=RANSAC(mpl,mpr,k=1000,t=10000,d=225,n=4)
    
    if H is None:
        print("solve H failure")
        exit(0)
    
    perspective_imgr=cv2.warpPerspective(imgr, H, (imgl.shape[1] + imgr.shape[1], imgl.shape[0]))
    cv2.imwrite('image/perspective_imgr.jpg',perspective_imgr)
    
    panoroma_image=perspective_imgr
    print(panoroma_image.shape)
    notblack=np.sum(panoroma_image,axis=2)
    for i in range(imgl.shape[0]):
        for j in range(imgr.shape[1]):
            if(notblack[i][j]==0):
                panoroma_image[i,j,:]=imgl[i,j,:]   
    
    cv2.imwrite('image/panoroma_image.jpg',panoroma_image)

if __name__=='__main__':
    main()