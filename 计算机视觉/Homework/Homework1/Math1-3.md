## 1.  

### Question: Prove set $\{ M_i\}$ forms a group.

$$
M_i=\begin{bmatrix} R_i& \bold{t}_i\\ \bold{0}^T&1 \end{bmatrix}\in\mathbb{R}^{4\times4},R_i\in \mathbb{R}^{3\times3} is \ an \ orthonormal \ matrix ,\det{( R_i)}=1.\\
\bold{t}_i\in\mathbb{R}^{3\times1}
$$

### Solution:

To  prove that $\{ M_i\}$satisfies the four properties of a group, i.e., the 

closure, the associativity, the existence of an identity element, and the existence of 

an inverse element for each group element.

##### The Closure:

$$
M_a\times M_b=\begin{bmatrix} R_a& \bold{t}_a\\ \bold{0}^T&1 \end{bmatrix} \begin{bmatrix} R_b& \bold{t}_b\\ \bold{0}^T&1 \end{bmatrix} 
=\begin{bmatrix} R_aR_b&  R_a\bold{t}_b+ \bold{t}_a\\ \bold{0}^T&1 \end{bmatrix}
$$

1. prove $R_aR_b$ is orthonormal.
   $$
   {(R_aR_b)}^T({R_aR_b})={R_b}^TR_a^TR_aR=I
   $$



2. prove $\det{(R_aR_b)}$ is 1.

   Because $R_a,R_b$ are $n\times n$ matrix,So

$$
\det{(R_aR_b)}=\det{(R_a)}\det{(R_b)}=1\times1=1
$$

3. And obviously,$R_a\bold{t}_b+ \bold{t}_a \in \mathbb{R}^{3\times1} $

   Therefore,$M_a\times M_b \in \{M_i\}$

Satisfied Closure.

**The Associativity**:
$$
(M_a\times M_b)\times M_c=(\begin{bmatrix} R_a& \bold{t}_a\\ \bold{0}^T&1 \end{bmatrix} \begin{bmatrix} R_b& \bold{t}_b\\ \bold{0}^T&1 \end{bmatrix})\begin{bmatrix} R_c& \bold{t}_c\\ \bold{0}^T&1 \end{bmatrix}
=\begin{bmatrix} R_aR_b&  R_a\bold{t}_b+ \bold{t}_a\\ \bold{0}^T&1 \end{bmatrix}\begin{bmatrix} R_c& \bold{t}_c\\ \bold{0}^T&1 \end{bmatrix}
\\=\begin{bmatrix} R_aR_bR_c&  R_aR_b\bold{t}_c+ R_a\bold{t}_b+\bold{t}_a\\ \bold{0}^T&1 \end{bmatrix}
$$

$$
M_a\times (M_b\times M_c)=\begin{bmatrix} R_a& \bold{t}_a\\ \bold{0}^T&1 \end{bmatrix} (\begin{bmatrix} R_b& \bold{t}_b\\ \bold{0}^T&1 \end{bmatrix}\begin{bmatrix} R_c& \bold{t}_c\\ \bold{0}^T&1 \end{bmatrix})
=\begin{bmatrix} R_a& \bold{t}_a\\ \bold{0}^T&1 \end{bmatrix}\begin{bmatrix} R_bR_c&  R_b\bold{t}_c+ \bold{t}_b\\ \bold{0}^T&1 \end{bmatrix}
\\=\begin{bmatrix} R_aR_bR_c&  R_aR_b\bold{t}_c+ R_a\bold{t}_b+\bold{t}_a\\ \bold{0}^T&1 \end{bmatrix}
$$



Therefore,$ (M_a\times M_b)\times M_c=M_a\times (M_b\times M_c)$

Satisfied Associativity.

**The Existence Of An Identity Element**

Let $E=\begin{bmatrix} I_3&\bold{0}\\ \bold{0}^T&1 \end{bmatrix}$
$$
E\times M_a=\begin{bmatrix} I_3&\bold{0}\\ \bold{0}^T&1 \end{bmatrix}\begin{bmatrix} R_a& \bold{t}_a\\ \bold{0}^T&1 \end{bmatrix}=\begin{bmatrix} R_a& \bold{t}_a\\ \bold{0}^T&1 \end{bmatrix}=M_a
$$

$$
M_a\times E=\begin{bmatrix} R_a& \bold{t}_a\\ \bold{0}^T&1 \end{bmatrix}\begin{bmatrix} I_3&\bold{0}\\ \bold{0}^T&1 \end{bmatrix}=\begin{bmatrix} R_a& \bold{t}_a\\ \bold{0}^T&1 \end{bmatrix}=M_a
$$

Satisfied Existing Identity Element.

**The Existence Of An Inverse Element For Each Group Element**

We can conclude,
$$
M_a^{-1}=\begin{bmatrix} R_a^{-1}& -R_a^{-1}\bold{t}_a\\ \bold{0}^T&1 \end{bmatrix} 
\\ \therefore M_a\times M_a^{-1}=I
$$

1. prove $R_a^{-1}$ is orthonormal.

   $I={(R_a^TR_a)}^{-1}=R_a^{-1}({R_a^{-1}})^T$,so  $R_a^{-1}$ is orthonormal.

2. prove $\det{(R_a^{-1})}$ is 1.

$$
\det{(R_a^{-1})}=\frac{1}{\det{(R_a)}}=1
$$

3. And obviously,$-R_a^{-1}\bold{t}_a\in \mathbb{R}^{3\times1} $

​	Therefore,$M_a^{-1}\in \{M_i\}$

​	Satisfied existence of An Inverse Element For Each Group Element.



## 2.

$$
M=\begin{bmatrix}\sum_{(x_i,y_i)\in w}{(I_x)}^2 & \sum_{(x_i,y_i)\in w}(I_xI_y) \\ \sum_{(x_i,y_i)\in w}(I_xI_y)& \sum_{(x_i,y_i)\in w}{(I_y)}^2\end{bmatrix}
$$



### a)prove that $M$ is positive semi-definite.

Prove:
$$
\because M=\begin{bmatrix}\sum_{(x_i,y_i)\in w}{(I_x)}^2 & \sum_{(x_i,y_i)\in w}(I_xI_y) \\ \sum_{(x_i,y_i)\in w}(I_xI_y)& \sum_{(x_i,y_i)\in w}{(I_y)}^2\end{bmatrix}=\sum_{(x_i,y_i)\in w}\begin{bmatrix}{(I_x)}^2 & (I_xI_y) \\ (I_xI_y)& {(I_y)}^2\end{bmatrix}=\sum_{(x_i,y_i)\in w}M(x_i,y_i)
\\
\because For\  all \ \boldsymbol{x} \in \mathbb{R}^{2\times1},\boldsymbol{x}^T M(x_i,y_i)\boldsymbol{x}={(x_1I_1+x_2I_2)}^2 \geq0
\\
\therefore For\  all \boldsymbol{x} \in \mathbb{R}^{2\times1},\boldsymbol{x}^T M\boldsymbol{x}=\boldsymbol{x}^T \sum_{(x_i,y_i)\in w}M(x_i,y_i) \boldsymbol{x}\geq0
\\
$$
So,$M$ is positive semi-definite.

### **b)**

For a formulation  $ ax^2+bxy+cy^2+dx+ey+f=0,\Delta=b^2-4ac<0 $ represents an ellipse.
$$
\begin{bmatrix}x&y\end{bmatrix}M\begin{bmatrix}x\\y\end{bmatrix}-1
=\sum_{(x_i,y_i)\in w}{(I_x)}^2 \times x^2+2\sum_{(x_i,y_i)\in w}(I_xI_y)\times xy+\sum_{(x_i,y_i)\in w}{(I_y)}^2\times y^2 -1\\
$$

$$
\therefore \Delta=b^2-4ac=4{(\sum_{(x_i,y_i)\in w}(I_xI_y))}^2-4(\sum_{(x_i,y_i)\in w}{(I_x)}^2)(\sum_{(x_i,y_i)\in w}{(I_y)}^2)
$$

Because $M$ is positive,So $det(M)>0$ holds.


$$
\therefore det(M)=(\sum_{(x_i,y_i)\in w}{(I_x)}^2)(\sum_{(x_i,y_i)\in w}{(I_y)}^2)-
{(\sum_{(x_i,y_i)\in w}(I_xI_y))}^2>0
\\
\therefore
{(\sum_{(x_i,y_i)\in w}(I_xI_y))}^2-(\sum_{(x_i,y_i)\in w}{(I_x)}^2)(\sum_{(x_i,y_i)\in w}{(I_y)}^2)<0
$$

So,$\begin{bmatrix}x&y\end{bmatrix}M\begin{bmatrix}x\\y\end{bmatrix}-1$  can represent an ellipse.

### **c)**

We can diagonalize symmetric matrices, 
$$
M=P^{T}\Lambda P=P^{-1}\Lambda P,
\\
\therefore PM=\Lambda P,
\\
\therefore \Lambda=\begin{bmatrix}\lambda_1&\\ & \lambda_2\end{bmatrix}
$$
So,
$$
\begin{bmatrix}x&y\end{bmatrix}M\begin{bmatrix}x\\y\end{bmatrix}-1=\begin{bmatrix}x&y\end{bmatrix}P^{T}\Lambda P\begin{bmatrix}x\\y\end{bmatrix}-1
=\begin{bmatrix}x'&y'\end{bmatrix}\Lambda\begin{bmatrix}x'\\y'\end{bmatrix}-1
\\
=\lambda_1{x'}^2+\lambda_2{y'}^2
$$
Because $P$ is an orthogonal matrix,$P\begin{bmatrix}x\\y\end{bmatrix}$​ means to do a rotation transformation for the point 

(𝑥, 𝑦) on the ellipse.

And,$\lambda_1{x'}^2+\lambda_2{y'}^2=\frac{{x'}^2}{\frac{1}{\lambda_1}}+\frac{{y'}^2}{\frac{1}{\lambda_2}}$,and $\lambda_1>\lambda_2>0,so \ \frac{1}{\lambda_1}<\frac{1}{\lambda_2}.$

So,**the length of** **its semi-major axis is**$\frac{1}{\lambda_2}$ **while the length of its semi-minor axis is** $\frac{1}{\lambda_1}$.

## 3.

### Question:

The condition is ,$A$ is a matrix of m$\times$ n,  $R(A)=n$$,A^TA$ is a matrix of $n\times n$.

And to prove $A^TA $ is non-singular,is to prove $R(A^TA)=n$. 

### Solution:

Consider the null space of $A$, denoted as $N(A)$. 

To prove $ N(A)=N(A^TA)$ 

1. Prove if $\boldsymbol{x}\in N(A)$,and $ \boldsymbol{x} \in N(A^TA)$
   $$
   \because A\boldsymbol{x}= \bf{0}
   \\
   \therefore A^TA\boldsymbol{x}= \bf{0}
   $$
   And it can be proved.

2. Prove if $\boldsymbol{x} \in N(A^TA)$,and $\boldsymbol{x} \in N(A)$
   $$
   \because A^TA\boldsymbol{x}=\boldsymbol{0}
   \\
   \therefore \boldsymbol{x}^T A^T A\boldsymbol{x}=\boldsymbol{0},and \ {(A\boldsymbol{x})}^TA\boldsymbol{x}=\boldsymbol{0}
   \\
   {||A\boldsymbol{x}||}^2=\boldsymbol{0}
   \\
   \therefore A\boldsymbol{x}=\boldsymbol{0}
   $$
   And it can be proved.

And $ N(A)=N(A^TA)$ can be proved. 

So $R(N(A^TA))=R(N(A))=0$.

There is a theorem:$B$ is a matrix of $m\times n$,and $R(B)=n-R(N(B))$.

Therefore,$R(A^TA)=n-R(N(A^TA))=n$

So  $A^TA $ is a full-rank matrix,which means $A^TA $ is non-singular matrix.

