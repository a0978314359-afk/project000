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
            angle_right, img = detector.findAngle(lmList[14], lmList[12],
                                            lmList[24], img)
            angle_left, img = detector.findAngle(lmList[13], lmList[11],
                                            lmList[23], img)
            
            bar_right = np.interp(angle_right, (20, 60), (w//2-100, w//2+100))
            cv2.rectangle(img, (w//2-100, 10), (int(bar_right), 50),
                               (0, 255, 0), cv2.FILLED)
            cv2.rectangle(img, (220, 10), (420, 50),
                                (255, 0, 0), 3)
            img = cv2AddChineseText(img, "右", (425, 10), (0, 0, 0), 40)

            bar_left = np.interp(angle_left, (20, 60), (w//2-100, w//2+100))
            cv2.rectangle(img, (w//2-100, 75), (int(bar_left), 115),
                               (0, 255, 0), cv2.FILLED)
            cv2.rectangle(img, (220, 75), (420, 115),
                                (255, 0, 0), 3)
            img = cv2AddChineseText(img, "左", (425, 75), (0, 0, 0), 40)

            if angle_left >= 60 and angle_right >= 60:
                if dir == 0:
                    count = count + 0.5
                    dir = 1 
            if angle_left <= 20 and angle_left <= 20:
                if dir == 1:
                    count = count + 0.5
                    dir = 0  
            msg = str(int(count))        
            cv2.putText(img, msg, (50, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 5,
                        (255, 255, 255), 10)
            
            coordinate = np.multiply(lmList[14], [1, 1]).astype(int)
            string1 = '非常完美'
            string2 = '內\n收\n雙\n臂\n，\n盡\n可\n能\n向\n前\n伸'
            string3 = '繼續往前伸'
            string4 = '再縮回來一點'
            if int(bar_right) == 220:
                img = cv2AddChineseText(img, string1, (coordinate[0],coordinate[1] - 75), (255, 255, 255), 30)
                cv2.rectangle(img, (coordinate[0] - 25, coordinate[1] - 100), (coordinate[0] + 150, coordinate[1] - 25), (0, 0, 0), 2)
            if int(bar_right) == 420:
                img = cv2AddChineseText(img, string2, (coordinate[0],coordinate[1] - 115), (255, 255, 255), 30)
                cv2.rectangle(img, (coordinate[0] - 25, coordinate[1] - 120), (coordinate[0] + 50, coordinate[1] + 225), (0, 0, 0), 2)
            if dir == 1 and int(bar_right) != 220:
                img = cv2AddChineseText(img, string3, (coordinate[0],coordinate[1] - 75), (255, 255, 255), 30)
                cv2.rectangle(img, (coordinate[0] - 25, coordinate[1] - 100), (coordinate[0] + 150, coordinate[1] - 25), (0, 0, 0), 2)
            if dir == 0 and int(bar_right) != 420:
                img = cv2AddChineseText(img, string4, (coordinate[0],coordinate[1] - 75), (255, 255, 255), 30)
                cv2.rectangle(img, (coordinate[0] - 25, coordinate[1] - 100), (coordinate[0] + 150, coordinate[1] - 25), (0, 0, 0), 2)


            coordinate = np.multiply(lmList[13], [1, 1]).astype(int)
            string1 = '非常完美'
            string2 = '內\n收\n雙\n臂\n，\n盡\n可\n能\n向\n前\n伸'
            string3 = '繼續往前伸'
            string4 = '再縮回來一點'
            if int(bar_left) == 220:
                img = cv2AddChineseText(img, string1, (coordinate[0],coordinate[1] - 75), (255, 255, 255), 30)
                cv2.rectangle(img, (coordinate[0] - 25, coordinate[1] - 100), (coordinate[0] + 150, coordinate[1] - 25), (0, 0, 0), 2)
            if int(bar_left) == 420:
                img = cv2AddChineseText(img, string2, (coordinate[0],coordinate[1] - 115), (255, 255, 255), 30)
                cv2.rectangle(img, (coordinate[0] - 25, coordinate[1] - 120), (coordinate[0] + 50, coordinate[1] + 225), (0, 0, 0), 2)
            if dir == 1 and int(bar_left) != 220:
                img = cv2AddChineseText(img, string3, (coordinate[0],coordinate[1] - 75), (255, 255, 255), 30)
                cv2.rectangle(img, (coordinate[0] - 25, coordinate[1] - 100), (coordinate[0] + 150, coordinate[1] - 25), (0, 0, 0), 2)
            if dir == 0 and int(bar_left) != 420:
                img = cv2AddChineseText(img, string4, (coordinate[0],coordinate[1] - 75), (255, 255, 255), 30)
                cv2.rectangle(img, (coordinate[0] - 25, coordinate[1] - 100), (coordinate[0] + 150, coordinate[1] - 25), (0, 0, 0), 2)

        cv2.imshow("Pose", img)        
    else:
        break
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
