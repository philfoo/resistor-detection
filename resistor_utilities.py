import numpy as np
import matplotlib.pyplot as plt
import cv2


def initializeEllipticSnake(height, width):
    s = np.linspace(0, 2.0*np.pi, 400.0)
    x = width/2.0 + width/3.0*np.cos(s)
    y = height/2.0 + height/3.0*np.sin(s)
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
    elif (max(rgb_values) - min(rgb_values) >= 30):
        if (np.argmax(rgb_values) == 0):
            return "red"
        elif (np.argmax(rgb_values) == 1):
            return "green"
        else:
            return "blue"
    else:
        return "black"


def findColorUsingHSV(rgb_values):
    blank_image = np.zeros((1,1,3), np.uint8)
    blank_image[:,:] = (rgb_values[2],rgb_values[1],rgb_values[0])      # (B, G, R)
    hsv_image = cv2.cvtColor(blank_image, cv2.COLOR_BGR2HSV)
    hue = hsv_image[0][0][0]/180.0*360.0
    sat = hsv_image[0][0][1]/256.0*100.0
    val = hsv_image[0][0][2]/256.0*100.0
    print (hue, sat, val)
    RED = 12
    BROWN = 28
    GOLD_VAL = 60
    ORANGE = 36
    ORANGE_SAT = 80
    ORANGE_VAL = 70
    YELLOW_SAT = 70
    YELLOW_VAL = 75
    YELLOW = 68
    GREEN = 144
    BLUE = 240
    VIOLET = 340
    WHITE_SAT = 50
    WHITE_VAL = 90
    SILVER_VAL = 80
    GRAY_VAL = 20
    BLACK_VAL = 20

    if (sat <= WHITE_SAT):
        if (val >= WHITE_VAL):
            return "white"
        elif (val >= SILVER_VAL):
            return "silver"
        elif (val >= GRAY_VAL):
            return "grey"
        else:
            return "black"
    elif (val <= BLACK_VAL):
        return "black"
    elif (hue >= VIOLET or hue <= RED):
        return "red"
    elif (hue >= RED and hue <= YELLOW):
        if (hue >= ORANGE and (sat >= YELLOW_SAT or val >= YELLOW_VAL)):
            return "yellow"
        elif (hue <= ORANGE and sat >= ORANGE_SAT and val >= ORANGE_VAL):
            return "orange"
        elif (hue >= BROWN and val >= GOLD_VAL):
            return "gold"
        else:
            return "brown"
    elif (hue >= YELLOW and hue <= GREEN):
        return "green"
    elif (hue >= GREEN and hue <= BLUE):
        return "blue"
    elif (hue >= BLUE and hue <= VIOLET):
        return "violet"
    else:
        return "brown"


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
