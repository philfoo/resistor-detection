import cv2
import sys
import numpy as np
from crop_rectangle import cropRectangle
from edge_math import edgeMath
from resistor_utilities import initializeEllipticSnake, displayResistance
from skimage.transform import rotate


if len(sys.argv) == 2:
    ### Reads image from a file
    img = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # img = rotate(img, 30, mode="edge")
    height, width, depth = img.shape

    init = initializeEllipticSnake(height, width)
    cropRectangle(img, init)
    resistance, tolerance = edgeMath("output.jpg")
    displayResistance(img, resistance, tolerance)

else:
    cap = cv2.VideoCapture(0)
    width = int(cap.get(3))
    height = int(cap.get(4))
    init = initializeEllipticSnake(height, width)
    pts = init.reshape((-1, 1, 2))
    initImg = np.zeros((height, width, 3), dtype='uint8')
    cv2.polylines(initImg, [pts], True, (0, 0, 255), thickness=5)

    while(True):
        ### Reads image from the computer camera
        ret, img = cap.read()
        cv2.imshow("Camera", cv2.add(initImg, img))

        k = cv2.waitKey(1)
        if k & 0xFF == ord('q'):
            break
        elif (k & 0xFF == ord('e')) or (k & 0xFF == ord(' ')):
            ### Convert to rgb since IMREAD_COLOR does bgr
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            cropRectangle(img, init)
            resistance, tolerance = edgeMath("output.jpg")
            displayResistance(img, resistance, tolerance)

    cap.release()
    cv2.destroyAllWindows()
