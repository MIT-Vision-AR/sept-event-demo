import cv2
import numpy as np
from tensorflow.python.keras.preprocessing import image
from tensorflow.python.keras.models import load_model
import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 8300
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
str = ""

model = load_model('gestures_v1.1.h5')
model.summary()


font = cv2.FONT_HERSHEY_SIMPLEX
cap = cv2.VideoCapture(0)
while (cap.isOpened()):
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    if ret == True:
        cv2.rectangle(frame, (300, 55), (600, 420), (225, 225, 225), 3)
        roi = frame[55:420, 300:600]
        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        roi = cv2.GaussianBlur(roi, (5, 5), cv2.BORDER_DEFAULT)

        cv2.imwrite('predict.jpg', roi)

        img_pred = image.load_img('predict.jpg', target_size=(150, 150, 1))
        img_pred = image.img_to_array(img_pred)
        img_pred = np.expand_dims(img_pred, axis=0)

        rslt = model.predict(img_pred)
        arr = np.rint(rslt)
        if(arr[0, 0] == 1):
            print("down")
            str = 'down'
            cv2.putText(roi, 'down', (50, 50), font,
                        2, (0, 255, 0), 3, cv2.LINE_AA)
        elif(arr[0, 1] == 1):
            print("fist")
            str = 'fist'
            cv2.putText(roi, 'fist', (50, 50), font,
                        2, (0, 255, 0), 3, cv2.LINE_AA)
        elif (arr[0, 2] == 1):
            print("left")
            str = 'left'
            cv2.putText(roi, 'left', (50, 50), font,
                        2, (0, 255, 0), 3, cv2.LINE_AA)
        elif (arr[0, 3] == 1):
            print("open")
            str = 'open'
            cv2.putText(roi, 'open', (50, 50), font,
                        2, (0, 255, 0), 3, cv2.LINE_AA)
        elif (arr[0, 4] == 1):
            print("right")
            str = 'right'
            cv2.putText(roi, 'right', (50, 50), font,
                        2, (0, 255, 0), 3, cv2.LINE_AA)
        else:
            print('up')
            str = 'up'
            cv2.putText(roi, 'up', (50, 50), font, 2,
                        (0, 255, 0), 3, cv2.LINE_AA)
        #cv2.imshow('', frame)
        cv2.imshow('roi', roi)
        cv2.imshow('sk', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        continue
    sock.sendto(str.encode(), (UDP_IP, UDP_PORT))
cap.release()
out.release()
cv2.destroyAllWindows()
