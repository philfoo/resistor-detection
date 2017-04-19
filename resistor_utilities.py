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
    WHITE = 240
    SILVER = 200
    GREY = 100
    SECONDARY = 40
    YELLOW = 160
    YELLOW_N = 100
    ORANGE_N = 50
    GOLD_2 = 110
    ZERO = 0
    print (rgb_values)
    #White
    if (rgb_values[0] >= WHITE and rgb_values[1] >= WHITE and rgb_values[2] >= WHITE):
        print ("white")
    #Silber
    elif (rgb_values[0] >= SILVER and rgb_values[1] >= SILVER and rgb_values[2] >= SILVER):
        print ("silver")
    #Violet
    elif (rgb_values[0] >= SECONDARY and rgb_values[1] <= SECONDARY and rgb_values[2] >= SECONDARY):
        print ("violet")
    #Yellow
    elif (rgb_values[0] >= YELLOW and rgb_values[1] >= YELLOW and rgb_values[2] <= YELLOW_N):
        print ("yellow")
    #Gold
    elif (rgb_values[0] >= YELLOW and rgb_values[1] >= GOLD_2 and rgb_values[2] <= YELLOW_N):
        print ("gold")
    #Orange
    elif (rgb_values[0] >= YELLOW and rgb_values[1] >= GREY and rgb_values[2] <= ORANGE_N):
        print ("orange")
    #Brown
    elif (rgb_values[0] >= GREY and rgb_values[1] >= ORANGE_N and rgb_values[2] <= SECONDARY):
        print ("brown")
    #Grey
    elif (rgb_values[0] >= GREY and rgb_values[1] >= GREY and rgb_values[2] >= GREY):
        print ("grey")
    #Red
    elif (max(rgb_values) - min(rgb_values) >= 20):
        if (np.argmax(rgb_values) == 0):
            print ("red")
        elif (np.argmax(rgb_values) == 1):
            print ("green")
        else:
            print ("blue")
    else:
        print ("black")
    return
