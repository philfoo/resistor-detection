import cv2
from crop_rectangle import cropRectangle

cap = cv2.VideoCapture(0)

while(True):
    ### Reads image from the computer camera
    ret, img = cap.read()

    ### Reads image from a file
    # img = cv2.imread("resistor-blue.jpg", cv2.IMREAD_COLOR)

    cropRectangle(img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
