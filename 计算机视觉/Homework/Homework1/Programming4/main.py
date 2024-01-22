import random
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
def homogeneousLinearSquares(A):
    
    U,S,V=np.linalg.svd(A.T@A,full_matrices=False)
    #full_matrices=False is a must,otherwise 
    #U is column orthogonal matrix,
    #V is row orthogonal matrix
    ans=V[-1]
 
    return ans
    
def RANSAC(points,k,t,d,n=2):

    bestFit=None
    bestErr=0x7ffffffffff #a num large enough

    for i in tqdm(range(k)):
     
        [index1,index2] = random.sample(range(points.shape[0]), n)
        
        p1=np.concatenate((points[index1], np.array([1])))
        p2=np.concatenate((points[index2], np.array([1])))
        A=np.array([p1,p2])

        #ax+by+c=0
        model= homogeneousLinearSquares(A)
        alsoInliers=[]
        
        for j in range(points.shape[0]):
            p=points[j]
            [a,b,c]=model
            distance=abs(a*p[0]+b*p[1]+c)/np.sqrt(a**2+b**2)# distance between a point and  a  line 
            if distance<t:
                alsoInliers.append(p)
        
        inlierNum=len(alsoInliers)
        #print(inlierNum)
        if inlierNum>=d:
            AB=np.array(alsoInliers)
            C=np.ones((inlierNum,1))
            
            A=np.c_[AB,C]
            betterModel= homogeneousLinearSquares(A)
            a,b,c=betterModel
            thisErr=0.0
            for j in range(points.shape[0]):
                p=points[j]
                thisErr+=abs(a*p[0]+b*p[1]+c)
            if thisErr<bestErr:
                bestFit=betterModel
                bestErr=thisErr
    return bestFit   
                
            


def main():
    max_iter_times = 10000
    fitting_threshold = 0.5
    inliner_num_threshold = 11
    points=[[-2, 0],[0, 0.9],[2, 2.0], [3, 6.5],[4, 2.9],[5, 8.8], [6, 3.95], [8, 5.03], [10, 5.97],[12, 7.1],[13, 1.2], [14, 8.2],[16, 8.5], [18, 10.1]]
    points=np.array(points)
    
    bestModel=RANSAC(points,max_iter_times,t=fitting_threshold,d=inliner_num_threshold)
    if bestModel is not None:
        
        plt.plot(points[:,0],points[:,1],'bo')
        a,b,c=bestModel
        print(a,b,c)
        if b==0:
            x_position=c/a
            plt.axvline(x=x_position, color='red', linestyle='--') 
        else :
            x=np.arange(-5,25)
            y=(-c-a*x)/b
            plt.plot(x,y,color='red', linestyle='--')
        plt.savefig("image/answer.png")    
        plt.show()
        plt.close()
    else:
        print("Fitting failure") 
    

if __name__=='__main__':
    main()

 