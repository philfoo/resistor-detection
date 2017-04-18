import numpy as np
import matplotlib.pyplot as plt
import cv2
from skimage.color import rgb2gray
from skimage import data
from skimage.filters import gaussian
from skimage.segmentation import active_contour

#img = data.astronaut()
img = cv2.imread("unnamed.png", cv2.IMREAD_COLOR)
img = rgb2gray(img)

s = np.linspace(0, 2*np.pi, 400)
x = 220 + 200*np.cos(s)
y = 200 + 200*np.sin(s)
init = np.array([x, y]).T

snake = active_contour(gaussian(img, 3),
                       init, alpha=0.015, beta=10, gamma=0.001)
x_avg = np.average(snake[:,0]);
ys = snake[(snake[:,0]>x_avg*0.9) & (snake[:,0]<x_avg*1.1),1]
ys_avg = np.average(ys)
ys_above = np.average(ys[ys>ys_avg])
ys_below = np.average(ys[ys<ys_avg])
xlt = np.min(snake[(snake[:,1]>ys_above*0.99),0])
xlb = np.min(snake[(snake[:,1]<ys_below*1.01),0])
xl = (xlt+xlb)/2
xrt = np.max(snake[(snake[:,1]>ys_above*0.99),0])
xrb = np.max(snake[(snake[:,1]<ys_below*1.01),0])
xr = (xrt+xrb)/2
a = np.linspace(xl,xr,100)
y1 = ys_above + 0*a
y2 = ys_below + 0*a


fig = plt.figure(figsize=(7, 7))
ax = fig.add_subplot(111)
plt.gray()
ax.imshow(img)
ax.plot(init[:, 0], init[:, 1], '--r', lw=3)
#ax.plot(snake[:, 0], snake[:, 1], '-b', lw=3)
ax.plot(a, y1, '-b', lw=3)
ax.plot(a, y2, '-g', lw=3)
ax.set_xticks([]), ax.set_yticks([])
ax.axis([0, img.shape[1], img.shape[0], 0])

######################################################################
# Here we initialize a straight line between two points, `(5, 136)` and
# `(424, 50)`, and require that the spline has its end points there by giving
# the boundary condition `bc='fixed'`. We furthermore make the algorithm
# search for dark lines by giving a negative `w_line` value.
'''
img = data.text()

x = np.linspace(5, 424, 100)
y = np.linspace(136, 50, 100)
init = np.array([x, y]).T


snake = active_contour(gaussian(img, 1), init, bc='fixed',
                       alpha=0.1, beta=1.0, w_line=-5, w_edge=0, gamma=0.1)

fig = plt.figure(figsize=(9, 5))
ax = fig.add_subplot(111)
plt.gray()
ax.imshow(img)
ax.plot(init[:, 0], init[:, 1], '--r', lw=3)
ax.plot(snake[:, 0], snake[:, 1], '-b', lw=3)
ax.set_xticks([]), ax.set_yticks([])
ax.axis([0, img.shape[1], img.shape[0], 0])
'''
plt.show()

