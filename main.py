import cv2
from cvzone.PoseModule import PoseDetector
import pyglet.media
import os
import requests


#cap = cv2.VideoCapture('http://192.168.1.30/mjpeg/1') # esp32cam
cap = cv2.VideoCapture(0) #webcam
cap.set(3, 1280)
cap.set(4, 720)

detector = PoseDetector()
sound = pyglet.media.load("alarm.wav", streaming=False)
people = False
img_count, breakcount = 0, 0

path = 'C://Users/ASUS/PycharmProjects/pose_estimation/img/'
url   = 'https://api.telegram.org/bot'
token = "18937023404:AAElxaqqlKkCGgQtBs6GYKI0iCtmzwdkWDID" #replace token bot
chat_id = "1234567890" #replace chat ID
caption = "People%20Detected!!!"

while True:
    success, img = cap.read()
    img = detector.findPose(img, draw=False)
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False)

    img_name = f'image_{img_count}.png'

    if bboxInfo:
        #-------------------------FULL SCREEN----------------------------
        cv2.rectangle(img, (700, 20), (1220, 80), (0, 0, 255), cv2.FILLED)
        cv2.putText(img, "PEOPLE DETECTED!!!", (710, 70),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)
        # -------------------------DEFAULT SCREEN--------------------------
        # cv2.rectangle(img, (120, 20), (470, 80), (0, 0, 255), cv2.FILLED)
        # cv2.putText(img, "PEOPLE DETECTED!!!", (130, 60),
        #             cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        breakcount += 1


        if breakcount >= 30:
            if people == False:
                img_count += 1
                sound.play()
                cv2.imwrite(os.path.join(path, img_name), img)
                files = {'photo': open(path + img_name, 'rb')}
                resp = requests.post(url + token + '/sendPhoto?chat_id=' + chat_id + '&caption=' + caption + '', files=files)
                print(resp.status_code)
                people = not people
    else:
        breakcount = 0
        if people:
            people = not people


    cv2.imshow("Image", img)
    cv2.waitKey(1)
