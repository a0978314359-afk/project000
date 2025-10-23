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
while True:
    success, img = cap.read()
    if success:
        img = cv2.resize(img, (640, 480))
        h, w, c = img.shape
        pose, img = detector.findPose(img, draw=True)
        if pose:
            lmList = pose["lmList"]
            knee_angle, img = detector.findAngle(lmList[24], lmList[26],
                                            lmList[28], img)
            angle, img = detector.findAngle(lmList[12], lmList[14],
                                            lmList[16], img)
            
            knee_loc = np.multiply(lmList[26], [1, 1]).astype(int)
            if knee_angle < 30:
                img = cv2AddChineseText(img, '膝蓋伸直一點', (knee_loc[0],knee_loc[1] - 75), (255, 255, 255), 30)
                cv2.rectangle(img, (knee_loc[0] - 25, knee_loc[1] - 100), (knee_loc[0] + 150, knee_loc[1] - 25), (0, 0, 0), 2)
            elif knee_angle > 40:
                img = cv2AddChineseText(img, '膝蓋彎曲一點', (knee_loc[0],knee_loc[1] - 75), (255, 255, 255), 30)
                cv2.rectangle(img, (knee_loc[0] - 25, knee_loc[1] - 100), (knee_loc[0] + 150, knee_loc[1] - 25), (0, 0, 0), 2)

            bar = np.interp(angle, (90, 125), (w//2-100, w//2+100))
            cv2.rectangle(img, (w//2-100, 50), (int(bar), 100),
                               (0, 255, 0), cv2.FILLED)
            cv2.rectangle(img, (220, 50), (420, 100),
                                (255, 0, 0), 3)
            
            if angle >= 125: 
                if dir == 0:
                    count = count + 0.5
                    dir = 1 
            if angle <= 90: 
                if dir == 1:
                    count = count + 0.5
                    dir = 0  
            msg = str(int(count))        
            cv2.putText(img, msg, (50, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 5,
                        (255, 255, 255), 10)
            
            coordinate = np.multiply(lmList[14], [1, 1]).astype(int)
            string1 = '非常完美'
            string2 = '可以夾背彎曲了'
            string3 = '繼續往前伸直'
            string4 = '加油，用力夾背拉'
            if int(bar) == 220:
                img = cv2AddChineseText(img, string1, (coordinate[0],coordinate[1] - 75), (255, 255, 255), 30)
                cv2.rectangle(img, (coordinate[0] - 25, coordinate[1] - 100), (coordinate[0] + 150, coordinate[1] - 25), (0, 0, 0), 2)
            if int(bar) == 420:
                img = cv2AddChineseText(img, string2, (coordinate[0],coordinate[1] - 75), (255, 255, 255), 30)
                cv2.rectangle(img, (coordinate[0] - 25, coordinate[1] - 100), (coordinate[0] + 200, coordinate[1] - 25), (0, 0, 0), 2)
            if dir == 0 and int(bar) != 420:
                img = cv2AddChineseText(img, string3, (coordinate[0],coordinate[1] - 75), (255, 255, 255), 30)
                cv2.rectangle(img, (coordinate[0] - 25, coordinate[1] - 100), (coordinate[0] + 150, coordinate[1] - 25), (0, 0, 0), 2)
            if dir == 1 and int(bar) != 220:
                img = cv2AddChineseText(img, string4, (coordinate[0],coordinate[1] - 75), (255, 255, 255), 30)
                cv2.rectangle(img, (coordinate[0] - 25, coordinate[1] - 100), (coordinate[0] + 300, coordinate[1] - 25), (0, 0, 0), 2)

        cv2.imshow("Pose", img)        
    else:
        break
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()