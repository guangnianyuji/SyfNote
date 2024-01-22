# 1   Math: prove that $L(\mathbf{h})$  is a strictly convex function 

Because  If a function *L*(**h**) is differentiable up to at least second order, *L* is strictly convex if its Hessian matrix is positive definite.

Therefore, we can prove Hessian matrix of  *L*(**h**)  is positive definite.

First, compute derivative of  *L*(**h**)  to the first order.(Jacobian matrix )
$$
\frac{\partial L(\mathbf{h})}{\partial \mathbf{h}}={(\mathbf{J}(\mathbf{x}))}^Tf(\mathbf{x})+{(\mathbf{J}(\mathbf{x}))}^T{\mathbf{J}(\mathbf{x})}\mathbf{h}+\mu\mathbf{h}
$$
Second, compute derivative of  *L*(**h**)  to the second order.(Hessian matrix )
$$
\frac{\partial L^2(\mathbf{h})}{\partial \mathbf{h}\mathbf{h}^T}={(\mathbf{J}(\mathbf{x}))}^T{\mathbf{J}(\mathbf{x})}+\mu \mathbf{I}
$$
Let $\mathbf{H}(\mathbf{h})=\frac{\partial L^2(\mathbf{h})}{\partial \mathbf{h}\mathbf{h}^T}$. To prove it is positive definite.

For all $\mathbf{x}\in \mathbb{R}^{n\times1}$, and $\mathbf{x} \neq \mathbf{0} $.
$$
\mathbf{x}^T\mathbf{H}(\mathbf{h})\mathbf{x}=\overbrace{\mathbf{x}^T{(\mathbf{J}(\mathbf{x}))}^T{\mathbf{J}(\mathbf{x})}\mathbf{x}}^{\geq0}+\overbrace{\mu \mathbf{x}^T\mathbf{x}}^{>0}>0
$$
And we can know  the Hessian Matrix of  *L*(**h**), $\mathbf{H}$ is positive definite. So  *L* is strictly convex.