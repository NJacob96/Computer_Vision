"""
Imports we need.
Note: You may _NOT_ add any more imports than these.
"""
import argparse
import imageio
import logging
import numpy as np
from PIL import Image


def load_image(filename):
    """Loads the provided image file, and returns it as a numpy array."""
    im = Image.open(filename)
    return np.array(im)


def create_gaussian_kernel(size, sigma=1.0):
    """
    Creates a 2-dimensional, size x size gaussian kernel.
    It is normalized such that the sum over all values = 1. 

    Args:
        size (int):     The dimensionality of the kernel. It should be odd.
        sigma (float):  The sigma value to use 

    Returns:
        A size x size floating point ndarray whose values are sampled from the multivariate gaussian.

    See:
        https://en.wikipedia.org/wiki/Multivariate_normal_distribution
        https://homepages.inf.ed.ac.uk/rbf/HIPR2/eqns/eqngaus2.gif
    """

    # Ensure the parameter passed is odd
    if size % 2 != 1:
        raise ValueError('The size of the kernel should not be even.')

    # TODO: Create a size by size ndarray of type float32
    # create a array of size * size of tyep float32
    rv = np.ndarray(shape=(size, size), dtype="float32")

    # TODO: Populate the values of the kernel. Note that the middle `pixel` should be x = 0 and y = 0.
    # create a 2D array iterator over row and column of size and calculate the value of x,y of each pixel
    for i in range(0, size):
        x = i - size // 2
        # -2, -1, 0,1,2
        for j in range(0, size):
            y = j - size // 2
            # -2, -1, 0,1,2
            # start at rv[0,0]
            #approximation of a Gaussian function
            rv[i, j] = np.exp(-(x * x + y * y) / (2.0 * sigma * sigma)) / (2.0 * np.pi * sigma * sigma)

    # TODO:  Normalize the values such that the sum of the kernel = 1
    rv /= rv.sum()

    return rv


def convolve_pixel(img, kernel, i, j):
    """
    Convolves the provided kernel with the image at location i,j, and returns the result.
    If the kernel stretches beyond the border of the image, it returns the original pixel.

    Args:
        img:        A 2-dimensional ndarray input image.
        kernel:     A 2-dimensional kernel to convolve with the image.
        i (int):    The row location to do the convolution at.
        j (int):    The column location to process.

    Returns:
        The result of convolving the provided kernel with the image at location i, j.
    """

    # First let's validate the inputs are the shape we expect...
    if len(img.shape) != 2:
        raise ValueError(
            'Image argument to convolve_pixel should be one channel.')
    if len(kernel.shape) != 2:
        raise ValueError('The kernel should be two dimensional.')
    if kernel.shape[0] % 2 != 1 or kernel.shape[1] % 2 != 1:
        raise ValueError(
            'The size of the kernel should not be even, but got shape %s' % (str(kernel.shape)))

    # TODO: determine, using the kernel shape, the ith and jth locations to start at.
    # print(kernel)
    # print(kernel.shape[0]) #return the length of 1D array within another array
    # print(img)
    up_ith = i - kernel.shape[0] // 2
    left_jth = j - kernel.shape[1] // 2
    down_ith = i + kernel.shape[0] // 2
    right_jth = j + kernel.shape[1] // 2

    # TODO: Check if the kernel stretches beyond the border of the image.
    if up_ith < 0 or left_jth < 0 or down_ith >= img.shape[0] or right_jth >= img.shape[1]:
        # TODO: if so, return the input pixel at that location.
        result = img[i, j]

    # TODO: perform the convolution.
    else:
        result = 0.0
        ki = kernel.shape[0] // 2
        kj = kernel.shape[1] // 2
        for ii in range(-ki, ki + 1):
            for jj in range(-kj, kj + 1):
                u = ii + ki
                v = jj + kj
                result += kernel[u, v] * img[i - ii, j - jj]

    return result


def convolve(img, kernel):
    """
    Convolves the provided kernel with the provided image and returns the results.

    Args:
        img:        A 2-dimensional ndarray input image.
        kernel:     A 2-dimensional kernel to convolve with the image.

    Returns:
        The result of convolving the provided kernel with the image at location i, j.
    """
    # TODO: Make a copy of the input image to save results
    results = np.ones(img.shape)
    # TODO: Populate each pixel in the input by calling convolve_pixel and return results.
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            results[i][j] = convolve_pixel(img, kernel, i, j)

    results = np.array(np.around(results), dtype="uint8")
    return results


def split(img):
    """
    Splits a image (a height x width x 3 ndarray) into 3 ndarrays, 1 for each channel.

    Args:
        img:    A height x width x 3 channel ndarray.

    Returns:
        A 3-tuple of the r, g, and b channels.
    """
    if img.shape[2] != 3:
        raise ValueError('The split function requires a 3-channel input image')
    # TODO: Implement me
    (r, g, b) = np.dsplit(img, img.shape[-1])
    r = r[:, :, 0]
    g = g[:, :, 0]
    b = b[:, :, 0]

    return (r, g, b)

def merge(r, g, b):
    """
    Merges three images (height x width ndarrays) into a 3-channel color image ndarrays.

    Args:
        r:    A height x width ndarray of red pixel values.
        g:    A height x width ndarray of green pixel values.
        b:    A height x width ndarray of blue pixel values.

    Returns:
        A height x width x 3 ndarray representing the color image.
    """
    # TODO: Implement me
    rgb = np.dstack((r,g,b))
    return rgb

"""
The main function
"""
if __name__ == '__main__':
    logging.basicConfig(
        format='%(levelname)s: %(message)s', level=logging.INFO)
    parser = argparse.ArgumentParser(
        description='Blurs an image using an isotropic Gaussian kernel.')
    parser.add_argument('input', type=str, help='The input image file to blur')
    parser.add_argument('output', type=str, help='Where to save the result')
    parser.add_argument('--sigma', type=float, default=1.0,
                        help='The standard deviation to use for the Guassian kernel')
    parser.add_argument('--k', type=int, default=5,
                        help='The size of the kernel.')

    args = parser.parse_args()

    # first load the input image
    logging.info('Loading input image %s' % (args.input))
    inputImage = load_image(args.input)

    # Split it into three channels
    logging.info('Splitting it into 3 channels')
    (r, g, b) = split(inputImage)

    # compute the gaussian kernel
    logging.info('Computing a gaussian kernel with size %d and sigma %f' %
                 (args.k, args.sigma))
    kernel = create_gaussian_kernel(args.k, args.sigma)

    # convolve it with each input channel
    logging.info('Convolving the first channel')
    r = convolve(r, kernel)
    logging.info('Convolving the second channel')
    g = convolve(g, kernel)
    logging.info('Convolving the third channel')
    b = convolve(b, kernel)

    # merge the channels back
    logging.info('Merging results')
    resultImage = merge(r, g, b)

    # save the result
    logging.info('Saving result to %s' % (args.output))
    imageio.imwrite(args.output, resultImage)
