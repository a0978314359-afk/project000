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
            angle, img = detector.findAngle(lmList[24], lmList[26],
                                            lmList[28], img)
            
            bar = np.interp(angle, (105, 165), (w//2-100, w//2+100))
            cv2.rectangle(img, (w//2-100, 50), (int(bar), 100),
                               (0, 255, 0), cv2.FILLED)
            cv2.rectangle(img, (220, 50), (420, 100),
                                (255, 0, 0), 3)
            
            if angle <= 105:
                if dir == 0:
                    count = count + 0.5
                    dir = 1 
            if angle >= 165:
                if dir == 1:
                    count = count + 0.5
                    dir = 0  
            msg = str(int(count))        
            cv2.putText(img, msg, (50, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 5,
                        (255, 255, 255), 10)
            
            coordinate = np.multiply(lmList[26], [1, 1]).astype(int)
            string1 = '非常完美'
            string2 = '可以做下一個深蹲動作了' 
            string3 = '繼續往下蹲'
            string4 = '加油，用力起來！'
            if int(bar) == 220:
                img = cv2AddChineseText(img, string1, (coordinate[0],coordinate[1] - 75), (255, 255, 255), 30)
                cv2.rectangle(img, (coordinate[0] - 25, coordinate[1] - 100), (coordinate[0] + 150, coordinate[1] - 25), (0, 0, 0), 2)
            if int(bar) == 420:
                img = cv2AddChineseText(img, string2, (coordinate[0],coordinate[1] - 75), (255, 255, 255), 30)
                cv2.rectangle(img, (coordinate[0] - 25, coordinate[1] - 100), (coordinate[0] + 325, coordinate[1] - 25), (0, 0, 0), 2)
            if dir == 0 and angle >= 105 and angle <= 165:
                img = cv2AddChineseText(img, string3, (coordinate[0],coordinate[1] - 75), (255, 255, 255), 30)
                cv2.rectangle(img, (coordinate[0] - 25, coordinate[1] - 100), (coordinate[0] + 175, coordinate[1] - 25), (0, 0, 0), 2)
            if dir == 1 and angle >= 105 and angle <= 165:
                img = cv2AddChineseText(img, string4, (coordinate[0],coordinate[1] - 75), (255, 255, 255), 30)
                cv2.rectangle(img, (coordinate[0] - 25, coordinate[1] - 100), (coordinate[0] + 275, coordinate[1] - 25), (0, 0, 0), 2)
        cv2.imshow("Pose", img)        
    else:
        break
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
