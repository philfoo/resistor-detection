import cv2
import numpy as np
import math
from collections import deque

magic_number = 39

#import image
img = cv2.imread("strip2.png")

height, width, depth = img.shape
print "The width is ", width
cross_section_array = [];
for i in range(0, width-1):
	blue_sum = 0;
	green_sum = 0;
	red_sum = 0;
	for j in range(0, height-1):
		blue_sum += img[j, i][0]
		green_sum += img[j, i][1]
		red_sum += img[j, i][2]
	blue_avg = blue_sum / height
	green_avg = green_sum / height
	red_avg = red_sum / height

	# round
	blue_avg = math.ceil(blue_avg*100)/100
	red_avg = math.ceil(red_avg*100)/100
	green_avg = math.ceil(green_avg*100)/100
	cross_section = [blue_avg, green_avg, red_avg]
	cross_section_array.append(cross_section)

#print (cross_section_array)

# sliding window size 5 ranges
window_size = width / magic_number
blue_ranges = []
red_ranges = []
green_ranges = []
total_ranges = []
#iterate through all rgb list
for i in range(0, len(cross_section_array)-1-window_size):
	# find min and max 
	max = -1
	min = 257
	for j in range(0, window_size):
		curr = cross_section_array[i+j][1]
		#print(curr)
		if curr > max:
			max = curr
		if curr < min:
			min = curr
	#if (min > max):
		#print (min, max)
	bdiff = int(round(max-min))
	#print(bdiff)
	blue_ranges.append(bdiff)



	# find min and max 
	red_max = -1
	red_min = 257

	for j in range(0, window_size):
		curr = cross_section_array[i+j][1]
		#print(curr)
		if curr > red_max:
			red_max = curr
		if curr < red_min:
			red_min = curr
	#if (min > max):
		#print (min, max)
	rdiff = int(round(red_max-red_min))
	#print(rdiff)
	red_ranges.append(rdiff)



	# find min and max 
	gmax = -1
	gmin = 257
	for j in range(0, window_size):
		curr = cross_section_array[i+j][1]
		#print(curr)
		if curr > gmax:
			gmax = curr
		if curr < gmin:
			gmin = curr
	#if (min > max):
		#print (min, max)
	gdiff = int(round(gmax-gmin))
	#print(gdiff)
	green_ranges.append(gdiff)

	totaldiff = bdiff+rdiff+gdiff
	print(totaldiff)
	total_ranges.append(totaldiff)


