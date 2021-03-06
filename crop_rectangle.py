import numpy as np
import matplotlib.pyplot as plt
import math
# from numpy import linalg
from skimage.color import rgb2gray, rgb2hsv, hsv2rgb
from skimage.filters import gaussian
from skimage.segmentation import active_contour
from skimage.transform import rotate
from skimage.transform import probabilistic_hough_line
from skimage.feature import canny
from skimage.io import imsave


def cropRectangle(img, init):
    preImg = img

    ## Threshold out non-tan colors
    '''
    img = rgb2hsv(img)
    for i, row in enumerate(img):
        for j, pixel in enumerate(row):
            if (pixel[0]<.05 or pixel[0]>.3 or pixel[1]<.1):
                img[i, j][2] = 0
    img = hsv2rgb(img)
    '''

    ### Rotate the image to make the resistor horizontal, probably only works if the orignal image is not rotated past 45 degrees in either direction
    imgGray = rgb2gray(img)
    edges = canny(imgGray)
    lines = probabilistic_hough_line(edges, threshold=10, line_length=100, line_gap=10)
    # longestLine = [[], []]
    # longestLineLength = 0
    # longestLineAngle = 0
    angles = []
    for line in lines:
        p0, p1 = line
        l = [[], []]
        l[0] = p0[0]-p1[0]
        l[1] = p0[1]-p1[1]
        # length = linalg.norm(l)
        angle = math.atan2(l[1], l[0])*180/math.pi
        angles.append(angle)
        # if length > longestLineLength:
        #     longestLine = l
        #     longestLineLength = length
        #     longestLineAngle = angle
    angles = list(filter(lambda a: not(not(a > 45 and a < 135) and not(a < -45 and a > -135)), angles))  # Only look at vertical-ish lines
    angleToRotate = 0
    if len(angles) != 0:
        angleToRotate = sum(angles)/float(len(angles)) - 90
    ### Can also try the below line for noisy backgrounds
    # angleToRotate = longestLineAngle - 180
    if (angleToRotate < 45 and angleToRotate > -45):
        img = rotate(img, angleToRotate, mode="edge")

    ### Run active countour and create bounding box
    snake = active_contour(gaussian(img, 3),
                           init, alpha=0.003, beta=10, gamma=0.001, w_line=0, w_edge=0.5, max_px_move=5.0)
    x_avg = np.average(snake[:,0]);
    ys = snake[(snake[:,0]>x_avg*0.8) & (snake[:,0]<x_avg*1.2),1]
    ys_avg = np.average(ys)
    ys_above = np.average(ys[ys>ys_avg])
    ys_above = (ys_above - ys_avg) * 0.8 + ys_avg
    ys_below = np.average(ys[ys<ys_avg])
    ys_below = (ys_below - ys_avg) * 0.8 + ys_avg
    xlt = np.min(snake[(snake[:,1]>ys_above*0.99),0])
    xlb = np.min(snake[(snake[:,1]<ys_below*1.01),0])
    xl = np.max([xlt,xlb])
    xrt = np.max(snake[(snake[:,1]>ys_above*0.99),0])
    xrb = np.max(snake[(snake[:,1]<ys_below*1.01),0])
    xr = np.min([xrt,xrb])
    a = np.linspace(xl,xr,100)
    y1 = ys_above + 0*a
    y2 = ys_below + 0*a

    ### Plot results
    fig, ((ax1, ax2), (ax3, ax)) = plt.subplots(nrows=2, ncols=2, figsize=(16, 9),
                                        sharex=True, sharey=True)
    ax.imshow(img)
    ax.set_title('Rotated and Active Countour', fontsize=20)
    ax.plot(init[:, 0], init[:, 1], '--r', lw=3)
    ax.plot(snake[:, 0], snake[:, 1], '-b', lw=3)
    ax.plot(a, y1, '-b', lw=3)
    ax.plot(a, y2, '-g', lw=3)
    ax.set_xticks([]), ax.set_yticks([])
    ax.axis([0, img.shape[1], img.shape[0], 0])
    ax2.imshow(edges)
    ax2.set_title('Canny Edges', fontsize=20)
    for line in lines:
            p0, p1 = line
            ax3.plot((p0[0], p1[0]), (p0[1], p1[1]))
    ax3.set_title('Probabilistic Hough Transform', fontsize=20)
    ax1.imshow(preImg)
    ax1.set_title('Input Image', fontsize=20)
    fig.tight_layout()
    plt.show()

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

    ### Write to file
    cropx0 = int(xl)
    cropx1 = int(xr)
    cropy0 = int(ys_below)
    cropy1 = int(ys_above)
    croppedImg = img[cropy0:cropy1, cropx0:cropx1]
    imsave("output.jpg", croppedImg)

    return croppedImg
