Project 2: Fun With Homography

In this project you will learn about homography matrices and use them to warp planar regions in images. 

The project consists of two major parts: rectification of a single planar region, and compositing of one planar region onto another.

All image parameters for skeleton functions are passed as 3D numpy arrays with shape (height, width, 3) for color images and (height, width, 1) for greyscale.

You will need to compute the eigendecomposition of a real-valued symmetric matrix. Numpy provides such a function: Numpy Eigendecomposition. NOTE that this function returns the eigenvectors as columns, not rows as one might expect. The i'th eigenvector is evecs[:, i].
