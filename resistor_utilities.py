import numpy as np
import matplotlib.pyplot as plt


def initializeEllipticSnake(height, width):
    s = np.linspace(0, 2*np.pi, 400)
    x = width/2 + width/3*np.cos(s)
    y = height/2 + height/3*np.sin(s)
    init = np.array([x, y]).T
    init = init.astype(int)
    return init


def displayResistance(img, resistance, tolerance):
    fig = plt.figure(figsize=(7, 7))
    ax = fig.add_subplot(111)
    ax.imshow(img)
    ax.set_xticks([]), ax.set_yticks([])
    ax.axis([0, img.shape[1], img.shape[0], 0])
    plt.text(img.shape[1]/5, img.shape[0]/5, "$" + str(resistance) + "\Omega \pm" + str(tolerance) + "\%$", fontsize=36)
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

    #White
    if (rgb_values[0] >= WHITE and rgb_values[1] >= WHITE and rgb_values[2] >= WHITE):
        return "white"
    #Silber
    elif (rgb_values[0] >= SILVER and rgb_values[1] >= SILVER and rgb_values[2] >= SILVER):
        return "silver"
    #Violet
    elif (rgb_values[0] >= SECONDARY and rgb_values[1] <= SECONDARY and rgb_values[2] >= SECONDARY):
        return "violet"
    #Yellow
    elif (rgb_values[0] >= YELLOW and rgb_values[1] >= YELLOW and rgb_values[2] <= YELLOW_N):
        return "yellow"
    #Gold
    elif (rgb_values[0] >= YELLOW and rgb_values[1] >= GOLD_2 and rgb_values[2] <= YELLOW_N):
        return "gold"
    #Orange
    elif (rgb_values[0] >= YELLOW and rgb_values[1] >= GREY and rgb_values[2] <= ORANGE_N):
        return "orange"
    #Brown
    elif (rgb_values[0] >= GREY and rgb_values[1] >= ORANGE_N and rgb_values[2] <= SECONDARY):
        return "brown"
    #Grey
    elif (rgb_values[0] >= GREY and rgb_values[1] >= GREY and rgb_values[2] >= GREY):
        return "grey"
    #Red
    elif (max(rgb_values) - min(rgb_values) >= 20):
        if (np.argmax(rgb_values) == 0):
            return "red"
        elif (np.argmax(rgb_values) == 1):
            return "green"
        else:
            return "blue"
    else:
        return "black"


def getColorDigit(color):
    return {
        'black': 0,
        'brown': 1,
        'red': 2,
        'orange': 3,
        'yellow': 4,
        'green': 5,
        'blue': 6,
        'violet': 7,
        'grey': 8,
        'white': 9,
    }.get(color, 4)


def getColorMultiplier(color):
    return {
        'black': 1,
        'brown': 10,
        'red': 100,
        'orange': 1000,
        'yellow': 10000,
        'green': 100000,
        'blue': 1000000,
        'violet': 10000000,
    }.get(color, 10)


def getColorTolerance(color):
    return {
        'brown': 1,
        'red': 2,
        'green': .5,
        'blue': .25,
        'violet': .1,
        'grey': .05,
        'gold': 5,
        'silver': 10,
    }.get(color, 5)
