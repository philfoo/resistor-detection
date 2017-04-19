import cv2
import numpy as np
import math
import heapq
from collections import deque
from collections import Counter
from matplotlib import pyplot as plt


def findColor(rgb_values):
	#Black
	print (rgb_values)
	if (rgb_values[0] >= 0 and rgb_values[0] < 15 and rgb_values[1] > 0 and rgb_values[1] < 15 and rgb_values[2] > 0 and rgb_values[2] < 15):
		print ("black")
	#Brown
	elif (rgb_values[0] >= 75 and rgb_values[0] <= 105 and rgb_values[1] >= 30 and rgb_values[1] <= 60 and rgb_values[2] >= 30 and rgb_values[2] <= 60):
		print ("brown")
	#Red
	elif (rgb_values[0] >= 240 and rgb_values[0] <= 255 and rgb_values[1] > 0 and rgb_values[1] < 15 and rgb_values[2] > 0 and rgb_values[2] < 15):
		print ("red")
	#Orange
	elif (rgb_values[0] >= 240 and rgb_values[0] <= 255 and rgb_values[1] >= 112 and rgb_values[1] <= 142 and rgb_values[2] >= 0 and rgb_values[2] <= 15):
		print ("orange")
	#Yellow
	elif (rgb_values[0] >= 240 and rgb_values[0] <= 255 and rgb_values[1] >= 240 and rgb_values[1] <= 255 and rgb_values[2] >= 0 and rgb_values[2] <= 15):
		print ("yellow")
	#Green
	elif (rgb_values[0] >= 0 and rgb_values[0] <= 15 and rgb_values[1] >= 240 and rgb_values[1] <= 255 and rgb_values[2] >= 0 and rgb_values[2] <= 15):
		print ("green")
	#Blue
	elif (rgb_values[0] >= 0 and rgb_values[0] <= 15 and rgb_values[1] >= 0 and rgb_values[1] <= 15 and rgb_values[2] >= 240 and rgb_values[2] <= 255):
		print ("blue")
	#Violet
	elif (rgb_values[0] >= 165 and rgb_values[0] <= 195 and rgb_values[1] >= 55 and rgb_values[1] <= 85 and rgb_values[2] >= 205 and rgb_values[2] <= 235):
		print ("violet")
	#Grey
	elif (rgb_values[0] >= 142 and rgb_values[0] <= 172 and rgb_values[1] >= 132 and rgb_values[1] <= 162 and rgb_values[2] >= 145 and rgb_values[2] <= 175):
		print ("grey")
	#White
	elif (rgb_values[0] >= 240 and rgb_values[0] <= 255 and rgb_values[1] >= 240 and rgb_values[1] <= 255 and rgb_values[2] >= 240 and rgb_values[2] <= 255):
		print ("white")
	return;

img_url = "test1.png"

#import image
img = cv2.imread(img_url, 0)
edges = cv2.Canny(img, 100, 200)

e_height, e_width = edges.shape

detected_columns = []

#find all pixels where an edge "might" be
for i in range(0, e_width):
	for j in range(0, e_height):
		if (edges[j, i] != 0):
			detected_columns.append(i)

#use buckets to group potential column locations
bucket_size = 1;
frequent_buckets = []
for i in range(0, len(detected_columns)):	
	bucket_value = (detected_columns[i]/bucket_size) * bucket_size
	frequent_buckets.append(bucket_value)
	#print bucket_value, " ", detected_columns[i]

#count number of occurrences in frequent_buckets
num_lines = 8;
most_frequent = Counter(frequent_buckets).most_common(num_lines)



#get the eight most common column values
eight_column_vals = []
for i in range(0, num_lines):
 	eight_column_vals.append(most_frequent[i][0])

eight_column_vals.sort()
print (eight_column_vals)

#find the 4 rgb values in the original image
original_img = cv2.imread(img_url)
height, width, depth = original_img.shape

final_colors = []
for i in range(0, int(num_lines/2)):
	left_bound = eight_column_vals[2*i]
	right_bound = eight_column_vals[(2*i)+1]

	blue_sum = 0;
	green_sum = 0;
	red_sum = 0;

	counter = 0;
	rgb_values = []
	for j in range(left_bound, right_bound+1):
		for k in range(0, height):
			blue_sum += original_img[k, j][0]
			green_sum += original_img[k, j][1]
			red_sum += original_img[k, j][2]

			counter+=1
	blue_avg = blue_sum / counter
	green_avg = green_sum / counter
	red_avg = red_sum / counter

	rgb_values.append(red_avg)
	rgb_values.append(green_avg)
	rgb_values.append(blue_avg)
	final_colors.append(rgb_values)

print (final_colors)

for i in range(0, int(num_lines/2)):
	findColor(final_colors[i])

plt.subplot(121), plt.imshow(img, cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(edges, cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.show()

# print edges