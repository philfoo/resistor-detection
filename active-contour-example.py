import numpy as np
import matplotlib.pyplot as plt
from skimage.color import rgb2gray, rgb2hsv, hsv2rgb
from skimage import data
from skimage import io
from skimage.filters import gaussian
from skimage.segmentation import active_contour
from skimage.measure import approximate_polygon
from skimage.measure import label, regionprops
from skimage.transform import rotate

# Test scipy version, since active contour is only possible
# with recent scipy version
import scipy
split_version = scipy.__version__.split('.')
if not(split_version[-1].isdigit()): # Remove dev string if present
        split_version.pop()
scipy_version = list(map(int, split_version))
new_scipy = scipy_version[0] > 0 or \
            (scipy_version[0] == 0 and scipy_version[1] >= 14)


img = io.imread('resistorbackground.jpg')
img = rotate(img, -25)
## Threshold out non-tan
img = rgb2hsv(img)for i, row in enumerate(img):
    for j, pixel in enumerate(row):
        if (pixel[0]<.05 or pixel[0]>.3 or pixel[1]<.1):
            img[i, j][2] = 0
img = hsv2rgb(img)
#########################

s = np.linspace(0, 2*np.pi, 400)
x = 250 + 200*np.cos(s)
y = 175 + 150*np.sin(s)
init = np.array([x, y]).T

if not new_scipy:
    print('You are using an old version of scipy. '
          'Active contours is implemented for scipy versions '
          '0.14.0 and above.')

if new_scipy:
    snake = active_contour(gaussian(img, 3),
                           init, alpha=0.03, beta=10, gamma=0.001, w_line=0, w_edge=0.5, max_px_move=1.0)
    #snakeRect = approximate_polygon(snake, tolerance=20)
    fig = plt.figure(figsize=(7, 7))
    ax = fig.add_subplot(111)
    plt.gray()
    ax.imshow(img)
    ax.plot(init[:, 0], init[:, 1], '--r', lw=3)
    ax.plot(snake[:, 0], snake[:, 1], '-b', lw=3)
    ax.set_xticks([]), ax.set_yticks([])
    ax.axis([0, img.shape[1], img.shape[0], 0])
    plt.show()
    print('ok')
