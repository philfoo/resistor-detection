import numpy as np
import matplotlib.pyplot as plt


def initializeEllipticSnake(height, width):
    s = np.linspace(0, 2*np.pi, 400)
    x = width/2 + width/3*np.cos(s)
    y = height/2 + height/3*np.sin(s)
    init = np.array([x, y]).T
    init = init.astype(int)
    return init


def displayResistance(img, resistance):
    fig = plt.figure(figsize=(7, 7))
    ax = fig.add_subplot(111)
    ax.imshow(img)
    ax.set_xticks([]), ax.set_yticks([])
    ax.axis([0, img.shape[1], img.shape[0], 0])
    plt.text(img.shape[1]/2, img.shape[0]/2, "$" + str(resistance) + "\Omega$", fontsize=36)
    plt.show()


def findColor(rgb_values):
    print (rgb_values)
    #Black
    if (rgb_values[0] >= 0 and rgb_values[0] < 15 and rgb_values[1] >= 0 and rgb_values[1] < 15 and rgb_values[2] >= 0 and rgb_values[2] < 15):
        print ("black")
    #Brown
    elif (rgb_values[0] >= 75 and rgb_values[0] <= 105 and rgb_values[1] >= 30 and rgb_values[1] <= 60 and rgb_values[2] >= 30 and rgb_values[2] <= 60):
        print ("brown")
    #Red
    elif (rgb_values[0] >= 240 and rgb_values[0] <= 255 and rgb_values[1] >= 0 and rgb_values[1] < 15 and rgb_values[2] >= 0 and rgb_values[2] < 15):
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
    else:
        print ("not detected")
    return;
    