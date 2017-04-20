import cv2
import numpy as np
from collections import deque

window_length = 5;

#import image
img = cv2.imread("strip.png")

height, width, depth = img.shape
cross_section_array = [];
for i in range(0, width):
	blue_sum = 0;
	green_sum = 0;
	red_sum = 0;
	for j in range(0, height):
		blue_sum += img[j, i][0]
		green_sum += img[j, i][1]
		red_sum += img[j, i][2]
	blue_avg = blue_sum / height
	green_avg = green_sum / height
	red_avg = red_sum / height
	cross_section = [blue_avg, green_avg, red_avg]
	cross_section_array.append(cross_section)

print cross_section_array

#looking at ranges
min = 999;
max = -999;
for i in range (0, window_length):
	if (cross_section_array[i][0] < min):
		min = cross_section_array[i][0]
	if (cross_section_array[i][0] > max):
		max = cross_section_array[i][0]

for i in range(window_length, len(cross_section_array)):
	range = abs(max-min)
	print range
	if(cross_section_array[i][0] < min):
		min = cross_section_array[i][0]
	if (cross_section_array[i][0] > max):
		max = cross_section_array[i][0]

# d = deque();
# window_sums = [0, 0, 0]
# #add previous values to the deque so far
# for i in range(0, window_length):
# 	# d.append(cross_section_array[i][0])
# 	for j in range(0, 2):
# 		window_sum[j] += cross_section_array[i][j]

# for i in range(window_length, len(cross_section_array)-1):
# 	average = window_sum_blue / window_length;
# 	print average
# 	window_sum_blue -= cross_section_array[i - window_length][0]
# 	window_sum_blue += cross_section_array[i][0]




