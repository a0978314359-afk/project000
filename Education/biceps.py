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

cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
cv2.namedWindow("Pose", cv2.WINDOW_NORMAL)



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
            angle, img = detector.findAngle(lmList[12], lmList[14],
                                            lmList[16], img)
            
            bar = np.interp(angle, (50, 150), (w//2-100, w//2+100))
            cv2.rectangle(img, (w//2-100, 50), (int(bar), 100), (0, 0, 255), cv2.FILLED)

            cv2.rectangle(img, (220, 50), (420, 100),
                                (255, 0, 0), 3)

            if angle >= 150: 
                if dir == 0:
                    count = count + 0.5
                    dir = 1
            if angle <= 50: 
                if dir == 1:
                    count = count + 0.5
                    dir = 0
            msg = str(int(count))        
            cv2.putText(img, msg, (50, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 5,
                        (255, 255, 255), 10)
            
            coordinate = np.multiply(lmList[14], [1, 1]).astype(int)

            string1 = '非常完美'
            string2 = '手可以向上彎舉了'
            string3 = '繼續往下'
            string4 = '加油，再上來一點！'
            if dir == 1 and angle >= 50 and angle <= 150:
                img = cv2AddChineseText(img, string4, (coordinate[0],coordinate[1] - 75), (255, 255, 255), 30)
                cv2.rectangle(img, (coordinate[0] - 25, coordinate[1] - 100), (coordinate[0] + 300, coordinate[1] - 25), (0, 0, 0), 2)
            if dir == 0 and angle <= 150 and angle >= 50:
                img = cv2AddChineseText(img, string3, (coordinate[0],coordinate[1] - 75), (255, 255, 255), 30)
                cv2.rectangle(img, (coordinate[0] - 25, coordinate[1] - 100), (coordinate[0] + 150, coordinate[1] - 25), (0, 0, 0), 2)

            if int(bar) == 220:
                img = cv2AddChineseText(img, string1, (coordinate[0],coordinate[1] - 75), (255, 255, 255), 30)
                cv2.rectangle(img, (coordinate[0] - 25, coordinate[1] - 100), (coordinate[0] + 150, coordinate[1] - 25), (0, 0, 0), 2)   
            if int(bar) == 420:
                img = cv2AddChineseText(img, string2, (coordinate[0],coordinate[1] - 75), (255, 255, 255), 30)
                cv2.rectangle(img, (coordinate[0] - 25, coordinate[1] - 100), (coordinate[0] + 250, coordinate[1] - 25), (0, 0, 0), 2)

        cv2.imshow("Pose", img)  
        cv2.imshow("Image", img)
count = 0
calories = 0  # 新增

from PoseModule import PoseDetector
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# ---- 中文文字顯示函數 ----
def cv2AddChineseText(img, text, position, textColor=(255, 255, 255), textSize=30):
    if isinstance(img, np.ndarray):
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    fontStyle = ImageFont.truetype("STHeiti Medium.ttc", textSize, encoding='utf-8')
    draw.text(position, text, textColor, font=fontStyle)
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

# ---- 初始化攝影機 ----
cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
cv2.namedWindow("Pose", cv2.WINDOW_NORMAL)

detector = PoseDetector()
dir = 0
count = 0
calories = 0  # 卡路里初始化

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.resize(img, (640, 480))
    h, w, c = img.shape

    # ---- 偵測姿勢 ----
    pose, img = detector.findPose(img, draw=True)
    if pose:
        lmList = pose["lmList"]
        angle, img = detector.findAngle(lmList[12], lmList[14], lmList[16], img)

        # ---- 進度條 ----
        bar = np.interp(angle, (50, 150), (w//2-100, w//2+100))
        cv2.rectangle(img, (w//2-100, 50), (int(bar), 100), (0, 0, 255), cv2.FILLED)  # 紅色進度條
        cv2.rectangle(img, (220, 50), (420, 100), (255, 0, 0), 3)  # 藍色外框

        # ---- 計數邏輯 ----
        if angle >= 150:
            if dir == 0:
                count += 0.5
                dir = 1
        if angle <= 50:
            if dir == 1:
                count += 0.5
                dir = 0

        # ---- 計算卡路里 ----
        calories = count * 0.5  # 每次完整動作約0.5 kcal，可自行調整

        # ---- 顯示計數 ----
        msg = str(int(count))
        cv2.putText(img, msg, (50, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 5,
                    (255, 255, 255), 10)

        # ---- 顯示卡路里 ----
        cal_text = f"Calories: {calories:.1f} kcal"
        cv2.putText(img, cal_text, (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5,
                    (0, 255, 255), 3)

        # ---- 中文提示文字 ----
        coordinate = np.multiply(lmList[14], [1, 1]).astype(int)
        string1 = '非常完美'
        string2 = '手可以向上彎舉了'
        string3 = '繼續往下'
        string4 = '加油，再上來一點！'

        if dir == 1 and 50 <= angle <= 150:
            img = cv2AddChineseText(img, string4, (coordinate[0], coordinate[1]-75), (255, 255, 255), 30)
            cv2.rectangle(img, (coordinate[0]-25, coordinate[1]-100), (coordinate[0]+300, coordinate[1]-25), (0, 0, 0), 2)
        if dir == 0 and 50 <= angle <= 150:
            img = cv2AddChineseText(img, string3, (coordinate[0], coordinate[1]-75), (255, 255, 255), 30)
            cv2.rectangle(img, (coordinate[0]-25, coordinate[1]-100), (coordinate[0]+150, coordinate[1]-25), (0, 0, 0), 2)
        if int(bar) == 220:
            img = cv2AddChineseText(img, string1, (coordinate[0], coordinate[1]-75), (255, 255, 255), 30)
            cv2.rectangle(img, (coordinate[0]-25, coordinate[1]-100), (coordinate[0]+150, coordinate[1]-25), (0, 0, 0), 2)
        if int(bar) == 420:
            img = cv2AddChineseText(img, string2, (coordinate[0], coordinate[1]-75), (255, 255, 255), 30)


cv2.waitKey(1)

count = 0
calories = 0  # 新增

...


    else:
        break
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


...


cap.release()
cv2.destroyAllWindows()


