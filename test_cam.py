import cv2

cap_1 = cv2.VideoCapture('http://192.168.1.11/mjpeg/1') #esp32cam
cap_2 = cv2.VideoCapture(0) #Webcam

while True:
    success, img_1 = cap_1.read()
    success, img_2 = cap_2.read()
    cv2.imshow("esp32cam", img_1)
    cv2.imshow("webcam", img_2)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cv2.destroyAllWindows()