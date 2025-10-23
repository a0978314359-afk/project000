import time
import math
from PoseModule import PoseDetector
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def cv2AddChineseText(img, text, position, textColor = (255, 255, 255), textSize = 30):
    if(isinstance(img, np.ndarray)):
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    fontStyle = ImageFont.truetype("STHeiti Medium.ttc", textSize, encoding = 'utf-8')
    draw.text(position, text, textColor, font=fontStyle)
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

cap = cv2.VideoCapture(0)
detector = PoseDetector()
dir = 0 
count = 0
start_time = time.time()
before_gametime = 4
countdown_time = 61

while True:
    success, img = cap.read()

    current_time = time.time()

    elapsed_time1 = current_time - start_time
    remaining_time1 = before_gametime - elapsed_time1

    s1 = math.floor(remaining_time1 % 60)
    if remaining_time1 > 1:
        if success:
            img = cv2.resize(img, (640, 480))
            h, w, c = img.shape
            pose, img = detector.findPose(img, draw=True)

            if pose:
                cv2.putText(img, str(s1), (250, 300),
                            cv2.FONT_HERSHEY_SIMPLEX, 8,
                            (0, 255, 255), 25)

                lmList = pose["lmList"]
                angle, img = detector.findAngle(lmList[12], lmList[14],
                                                lmList[16], img)
                
                bar = np.interp(angle, (80, 160), (w//2-100, w//2+100))
                cv2.rectangle(img, (w//2-100, 50), (int(bar), 100),
                                (0, 255, 0), cv2.FILLED)
                cv2.rectangle(img, (220, 50), (420, 100),
                                (255, 0, 0), 3)
                
                msg = str(int(count))        
                cv2.putText(img, msg, (50, 150),
                            cv2.FONT_HERSHEY_SIMPLEX, 5,
                            (255, 255, 255), 10)
                
            cv2.imshow("Pose", img)        
        else:
            break
    elif remaining_time1 > 0 and remaining_time1 < 1:
        if success:
            img = cv2.resize(img, (640, 480))
            h, w, c = img.shape
            pose, img = detector.findPose(img, draw=True)

            if pose:
                cv2.putText(img, 'GO!!', (100, 300),
                            cv2.FONT_HERSHEY_SIMPLEX, 8,
                            (0, 255, 255), 25)

                lmList = pose["lmList"]
                angle, img = detector.findAngle(lmList[12], lmList[14],
                                                lmList[16], img)
                
                bar = np.interp(angle, (80, 160), (w//2-100, w//2+100))
                cv2.rectangle(img, (w//2-100, 50), (int(bar), 100),
                                (0, 255, 0), cv2.FILLED)
                cv2.rectangle(img, (220, 50), (420, 100),
                                (255, 0, 0), 3)
                
                msg = str(int(count))        
                cv2.putText(img, msg, (50, 150),
                            cv2.FONT_HERSHEY_SIMPLEX, 5,
                            (255, 255, 255), 10)
                
            cv2.imshow("Pose", img)        
        else:
            break
    else:
        elapsed_time = current_time - (start_time + before_gametime)
        remaining_time = countdown_time - elapsed_time

        if success and remaining_time > 0:
            img = cv2.resize(img, (640, 480))
            h, w, c = img.shape
            pose, img = detector.findPose(img, draw=True)

            if pose:
                m = remaining_time // 60
                s = math.floor(remaining_time % 60)
                min_sec_format = '{:0>2.0f}:{:0>2.0f}'.format(m, s)
                cv2.rectangle(img, (450,0), (640,50), (0, 0, 0), -1)
                img = cv2AddChineseText(img, min_sec_format, (475,0), (255, 255, 255), 60)

                lmList = pose["lmList"]
                angle, img = detector.findAngle(lmList[12], lmList[14],
                                                lmList[16], img)
                
                bar = np.interp(angle, (80, 160), (w//2-100, w//2+100))
                cv2.rectangle(img, (w//2-100, 50), (int(bar), 100),
                                (0, 255, 0), cv2.FILLED)
                cv2.rectangle(img, (220, 50), (420, 100),
                                (255, 0, 0), 3)
                
                if angle <= 80: 
                    dir = 1 
                if angle >= 160: 
                    if dir == 1:
                        count = count + 1
                        dir = 0  
                msg = str(int(count))        
                cv2.putText(img, msg, (50, 150),
                            cv2.FONT_HERSHEY_SIMPLEX, 5,
                            (255, 255, 255), 10)

            cv2.imshow("Pose", img)        
        else:
            break
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()