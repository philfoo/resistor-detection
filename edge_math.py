import cv2
import numpy as np
import math
from collections import deque
import matplotlib.pyplot as plt
from skimage.filters import sobel
from skimage.color.adapt_rgb import adapt_rgb, each_channel
from skimage import exposure
from resistor_utilities import findColor

### Constant for thresholding the sobel edges result
VAL_THRESHOLD_ENTER = 0.3
VAL_THRESHOLD_EXIT = 0.2
magic_number = 39
num_lines = 8


### Allows running of sobel filters on RGB images
@adapt_rgb(each_channel)
def sobel_each(image):
    return sobel(image)


def edgeMath(croppedImg):
    #import image
    img = cv2.imread(croppedImg)
    # img = cv2.imread("resistor-images/noisy_strip1.jpg")
    # img = croppedImg

    ### Average columns of individual RGB channels
    height, width, depth = img.shape
    print ("The width is ", width)
    r_array = np.zeros(0, dtype=np.uint8)
    g_array = np.zeros(0, dtype=np.uint8)
    b_array = np.zeros(0, dtype=np.uint8)
    for i in range(0, width-1):
        red_sum = 0
        green_sum = 0
        blue_sum = 0
        for j in range(0, height-1):
            red_sum += img[j, i][2]
            green_sum += img[j, i][1]
            blue_sum += img[j, i][0]
        blue_avg = blue_sum / height
        green_avg = green_sum / height
        red_avg = red_sum / height

        # round
        blue_avg = blue_avg/256
        red_avg = red_avg/256
        green_avg = green_avg/256
        b_array = np.append(b_array, blue_avg)
        g_array = np.append(g_array, green_avg)
        r_array = np.append(r_array, red_avg)

    ### Merge RGB channels, for some reason this makes the resistor vertical
    b, g, r = cv2.split(img)
    cross_section_array = cv2.merge((r_array, g_array, b_array))

    ### Stretch the image horizontally to see it better
    cross_section_array = np.tile(cross_section_array, (20, 1))
    # print (cross_section_array)
    # print (img)

    ### Apply a Sobel filter to detect color transitions
    edge_sobel = sobel_each(cross_section_array)

    ### Stretch the histogram to make edges more visible
    p2 = np.percentile(edge_sobel, 2)
    p98 = np.percentile(edge_sobel, 98)
    edge_eq = exposure.rescale_intensity(edge_sobel, in_range=(p2, p98))

    ### Extract the 16 color transitions
    height, width, depth = edge_eq.shape
    borders = []
    inborder = False
    for i in range(1, height-2):
        edge_val = max(edge_eq[i][1][0], edge_eq[i][1][1], edge_eq[i][1][2])
        if (not(inborder) and edge_val > VAL_THRESHOLD_ENTER):
            borders.append(i)
            inborder = True
        elif (inborder and edge_val < VAL_THRESHOLD_EXIT):
            borders.append(i)
            inborder = False
        # print (edge_val)
    print (borders)

    ### Plot result
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(16, 9),
                                        sharex=True, sharey=True)
    ax1.imshow(cross_section_array)
    ax1.set_title('Averaged RGB Values', fontsize=20)
    ax2.imshow(edge_sobel)
    ax2.set_title('Sobel Filter', fontsize=20)
    ax3.imshow(edge_eq)
    ax3.set_title('Contrast Stretching on Sobel Filter', fontsize=20)
    fig.tight_layout()
    plt.show()

    ### Get the RGB color values in between the borders
    try:
        eight_column_vals = [borders[1], borders[2], borders[5], borders[6], borders[9], borders[10], borders[13], borders[14]]
        print (eight_column_vals)
    except IndexError:
        print ("Detected less than 4 stripes!")
        return

    final_colors = []
    for i in range(0, int(num_lines/2)):
        top_bound = eight_column_vals[2*i]
        bottom_bound = eight_column_vals[(2*i)+1]
        blue_sum = 0
        green_sum = 0
        red_sum = 0
        counter = 0
        rgb_values = []
        for j in range(top_bound, bottom_bound+1):
            blue_sum += cross_section_array[j][1][2]
            green_sum += cross_section_array[j][1][1]
            red_sum += cross_section_array[j][1][0]
            counter += 1
        blue_avg = blue_sum / counter * 256
        green_avg = green_sum / counter * 256
        red_avg = red_sum / counter * 256
        rgb_values.append(red_avg)
        rgb_values.append(green_avg)
        rgb_values.append(blue_avg)
        final_colors.append(rgb_values)

    ### Map 4 RGB values to resistor band colors
    for i in range(0, int(num_lines/2)):
        findColor(final_colors[i])

    ### Return resistance
    return 9999

    # # sliding window size 5 ranges
    # window_size = width / magic_number
    # blue_ranges = []
    # red_ranges = []
    # green_ranges = []
    # total_ranges = []
    # #iterate through all rgb list
    # for i in range(0, len(cross_section_array)-1-window_size):
    #     # find min and max 
    #     max = -1
    #     min = 257
    #     for j in range(0, window_size):
    #         curr = cross_section_array[i+j][1]
    #         #print(curr)
    #         if curr > max:
    #             max = curr
    #         if curr < min:
    #             min = curr
    #     #if (min > max):
    #         #print (min, max)
    #     bdiff = int(round(max-min))
    #     #print(bdiff)
    #     blue_ranges.append(bdiff)



    #     # find min and max 
    #     red_max = -1
    #     red_min = 257

    #     for j in range(0, window_size):
    #         curr = cross_section_array[i+j][1]
    #         #print(curr)
    #         if curr > red_max:
    #             red_max = curr
    #         if curr < red_min:
    #             red_min = curr
    #     #if (min > max):
    #         #print (min, max)
    #     rdiff = int(round(red_max-red_min))
    #     #print(rdiff)
    #     red_ranges.append(rdiff)



    #     # find min and max 
    #     gmax = -1
    #     gmin = 257
    #     for j in range(0, window_size):
    #         curr = cross_section_array[i+j][1]
    #         #print(curr)
    #         if curr > gmax:
    #             gmax = curr
    #         if curr < gmin:
    #             gmin = curr
    #     #if (min > max):
    #         #print (min, max)
    #     gdiff = int(round(gmax-gmin))
    #     #print(gdiff)
    #     green_ranges.append(gdiff)

    #     totaldiff = bdiff+rdiff+gdiff
    #     print(totaldiff)
    #     total_ranges.append(totaldiff)
