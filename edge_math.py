import cv2
import numpy as np
# import math
# from collections import deque
from statistics import median
import matplotlib.pyplot as plt
from scipy.signal import medfilt
from skimage.filters import sobel
from skimage.color.adapt_rgb import adapt_rgb, each_channel
from skimage import exposure
from resistor_utilities import findColorUsingHSV, getColorDigit, getColorMultiplier, getColorTolerance

### Constant for thresholding the sobel edges result
VAL_THRESHOLD_ENTER = 0.2
VAL_THRESHOLD_EXIT = 0.15
### Number of pixels for the median filter to look at
MEDIAN_KERNEL = 25
num_lines = 8


### Allows running of sobel filters on RGB images
@adapt_rgb(each_channel)
def sobel_each(image):
    return sobel(image)


def edgeMath(croppedImg):
    #import image
    img = cv2.imread(croppedImg)
    # img = cv2.medianBlur(img,21)
    # img = cv2.imread("resistor-images/noisy_strip1.jpg")
    # img = croppedImg

    ### Take median for each column of individual RGB channels
    height, width, depth = img.shape
    print ("The width is ", width)
    r_array = np.zeros(0, dtype=np.uint8)
    g_array = np.zeros(0, dtype=np.uint8)
    b_array = np.zeros(0, dtype=np.uint8)
    for i in range(0, width-1):
        red_vals = []
        green_vals = []
        blue_vals = []
        for j in range(0, height-1):
            red_vals.append(int(img[j, i][2]))
            green_vals.append(int(img[j, i][1]))
            blue_vals.append(int(img[j, i][0]))
        blue_avg = median(blue_vals)/256.0
        green_avg = median(green_vals)/256.0
        red_avg = median(red_vals)/256.0
        b_array = np.append(b_array, blue_avg)
        g_array = np.append(g_array, green_avg)
        r_array = np.append(r_array, red_avg)

    ### Apply a median filter on each channel in 1D
    r_array = medfilt(r_array, MEDIAN_KERNEL)
    g_array = medfilt(g_array, MEDIAN_KERNEL)
    b_array = medfilt(b_array, MEDIAN_KERNEL)

    ### Merge RGB channels, for some reason this makes the resistor vertical
    cross_section_array = cv2.merge((r_array, g_array, b_array))

    ### Stretch the image horizontally to see it better
    cross_section_array = np.tile(cross_section_array, (20, 1))

    ### Apply a Sobel filter to detect color transitions
    edge_sobel = sobel_each(cross_section_array)

    ### Stretch the histogram to make edges more visible
    p2 = np.percentile(edge_sobel, 2)
    p98 = np.percentile(edge_sobel, 98)
    edge_eq = exposure.rescale_intensity(edge_sobel, in_range=(p2, p98))

    ### Extract the 16 color transitions
    height, width, depth = edge_eq.shape
    cushion = height/20.0
    borders = []
    inborder = False
    for i in range(1, height-2):
        edge_val = max(edge_eq[i][1][0], edge_eq[i][1][1], edge_eq[i][1][2])
        if (not(inborder) and edge_val > VAL_THRESHOLD_ENTER):
            ### Make sure each band is at least 5% of the height of the image away from the next
            if (len(borders) < 2 or i > (borders[-2]+cushion)):
                borders.append(i)
                inborder = True
        elif (inborder and edge_val < VAL_THRESHOLD_EXIT):
            borders.append(i)
            inborder = False
    print (borders)

    ### Plot result
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(16, 9),
                                        sharex=True, sharey=True)
    ax1.imshow(cross_section_array)
    ax1.set_title('Median RGB Values', fontsize=20)
    ax2.imshow(edge_sobel)
    ax2.set_title('Sobel Filter Over RGB Channels', fontsize=20)
    ax3.imshow(edge_eq)
    ax3.set_title('Contrast Stretching on Sobel Filter', fontsize=20)
    fig.tight_layout()
    plt.show()

    ### Try discovering the inner borders of the color bands
    try:
        ### If even number of extra bands assume correct bands are in the middle
        if (len(borders) > 16 and len(borders) % 4 == 0):
            middle = int(len(borders) / 2)
            borders = borders[middle-8:middle+8+1]
        eight_column_vals = [borders[1], borders[2], borders[5], borders[6], borders[9], borders[10], borders[13], borders[14]]
        print (eight_column_vals)
    except IndexError:
        print ("Detected less than 4 stripes! Assuming that the outer bands are at the edges.")
        try:
            eight_column_vals = [0, borders[0], borders[3], borders[4], borders[7], borders[8], borders[11], height-1]
        except IndexError:
            print ("Still not enough stripes. Aborting.")
            return

    ### Get the median RGB color values in between the borders
    final_colors = []
    for i in range(0, int(num_lines/2)):
        top_bound = eight_column_vals[2*i]
        bottom_bound = eight_column_vals[(2*i)+1]
        blue_vals = []
        green_vals = []
        red_vals = []
        rgb_values = []
        for j in range(top_bound, bottom_bound+1):
            blue_vals.append(cross_section_array[j][1][2])
            green_vals.append(cross_section_array[j][1][1])
            red_vals.append(cross_section_array[j][1][0])
        blue_avg = median(blue_vals) * 256
        green_avg = median(green_vals) * 256
        red_avg = median(red_vals) * 256
        rgb_values.append(red_avg)
        rgb_values.append(green_avg)
        rgb_values.append(blue_avg)
        final_colors.append(rgb_values)

    ### Map 4 RGB values to resistor band colors
    colors = []
    for i in range(0, int(num_lines/2)):
        colors.append(findColorUsingHSV(final_colors[i]))

    ### TODO: relax the assumption that one of the ends of the resistor will be gold or silver
    if (not(colors[0] == "gold" or colors[0] == "silver" or colors[-1] == "gold" or colors[-1] == "silver")):
        print ("Creating a gold...")
        if (colors[-1] == "brown" or colors[-1] == "grey"):
            colors[-1] = "gold"
        elif (colors[0] == "brown" or colors[-1] == "grey"):
            colors[0] = "gold"
    ### Make sure the gold/silver at the end of the list
    if (colors[0] == "gold" or colors[0] == "silver"):
        colors = colors[::-1]
    print (colors)

    ### Map colors to numerical meaning
    colorNumbers = []
    colorNumbers.append(getColorDigit(colors[0]))
    colorNumbers.append(getColorDigit(colors[1]))
    colorNumbers.append(getColorMultiplier(colors[2]))
    colorNumbers.append(getColorTolerance(colors[3]))

    ### Calculare resistance and tolerance
    resistance = (10*colorNumbers[0]+colorNumbers[1])*colorNumbers[2]
    tolerance = colorNumbers[3]

    ### Return resistance
    return resistance, tolerance
