import time
import numpy as np
import cv2

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
cap = cv2.VideoCapture(0)

while True:
   
     ret, frame = cap.read()
     flipped = cv2.flip(frame, flipCode = 1)
     frame1 = cv2.resize(flipped, (640, 480))
     font = cv2.FONT_HERSHEY_SIMPLEX
     gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
     boxes, weights = hog.detectMultiScale(frame1, winStride=(8,8) )
     boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
    
     for (xA, yA, xB, yB) in boxes:
        
        cv2.rectangle(frame1, (xA, yA), (xB, yB),(0, 255, 0), 2)
        b=len(boxes)
        cv2.putText(frame1,"people count : "+str(b),(20,50),0,2,(255,0,0),3)
     img = cv2.resize(frame1,(640,480))
     cv2.imshow("cam", frame1);
     if cv2.waitKey(1) & 0XFF == 27:
        break

frame1.release()
cv2.destroyAllWindows()
