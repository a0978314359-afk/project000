import cv2
import mediapipe as mp
import math


class PoseDetector:
    """
    Estimates Pose points of a human body using the mediapipe library.
    """

    def __init__(self, mode=False, smooth=True,
                 detectionCon=0.5, trackCon=0.5):
        """
        :param mode: In static mode, detection is done on each image: slower
        :param smooth: Smoothness Flag
        :param detectionCon: Minimum Detection Confidence Threshold
        :param trackCon: Minimum Tracking Confidence Threshold
        """

        self.mode = mode
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils # MediaPipe 提供的繪圖工具
        self.mpPose = mp.solutions.pose # MediaPipe 的姿勢偵測解決方案
        # 初始化 MediaPipe Pose 模型
        self.pose = self.mpPose.Pose(static_image_mode=self.mode,
                                     smooth_landmarks=self.smooth,
                                     min_detection_confidence=self.detectionCon,
                                     min_tracking_confidence=self.trackCon)
        self.lmList = [] # 初始化一個空的列表，用於儲存關鍵點座標（但在 findPose 中未使用此實例變數，而是用了局部變數 mylmList）

    def findPose(self, img, draw=True, bboxWithHands=False):
        """
        Find the pose landmarks in an Image of BGR color space.
        :param img: Image to find the pose in.
        :param draw: Flag to draw the output on the image.
        :return: Image with or without drawings
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # MediaPipe 需要 RGB 格式的影像
        self.results = self.pose.process(imgRGB) # 進行姿勢偵測處理
        mylmList = [] # 儲存這一幀偵測到的關鍵點座標 (x, y)
        poseInfo = {} # 儲存關於姿勢的資訊 (關鍵點列表, 邊界框, 中心點)

        if self.results.pose_landmarks: # 如果偵測到姿勢關鍵點
            for id,lm in enumerate(self.results.pose_landmarks.landmark): # 遍歷所有偵測到的關鍵點
                h, w, c = img.shape # 獲取影像的高、寬、channel(RGB 彩色圖片的 channel 是 3，灰階圖片則為 1）
                cx, cy = int(lm.x * w), int(lm.y * h) # 將整張圖寬度的百分比 (0.0-1.0) 轉換為實際上你在畫面上看到的 pixel 座標
                mylmList.append([cx, cy])

            # 計算邊界框 (Bounding Box)
            ad = abs(mylmList[12][0] - mylmList[11][0]) // 2 # 根據左右肩(11,12)的水平距離計算一個偏移量
            # 根據 bboxWithHands 決定 x 座標的計算方式
            if bboxWithHands:
                # 考慮手腕(15,16)的位置
                if mylmList[15][0] > mylmList[16][0]:
                    x1 = mylmList[16][0] - ad
                    x2 = mylmList[15][0] + ad
                else:
                    x1 = mylmList[15][0] - ad
                    x2 = mylmList[16][0] + ad
            else:
                # 考慮肩膀(11,12)的位置
                if mylmList[11][0] > mylmList[12][0]:
                    x1 = mylmList[12][0] - ad
                    x2 = mylmList[11][0] + ad
                else:
                    x1 = mylmList[11][0] - ad
                    x2 = mylmList[12][0] + ad

            # y 座標的計算
            y1 = mylmList[1][1] - ad # Landmark 1(left eye inner)，接近頭部最上方的位置，所以用它作為上邊界的參考點，-ad讓他往上擴張
            # Landmark 29, 30 是腳跟，作為下邊界的參考點
            if mylmList[30][1] > mylmList[29][1]:
                y2 = mylmList[30][1] + ad
            else:
                y2 = mylmList[29][1] + ad
            # 確保邊界框不超出影像範圍
            if x1 < 0: x1 = 0
            if y1 < 0: y1 = 0
            bbox = (x1, y1, x2 - x1, y2 - y1) # 邊界框 (x, y, 寬度, 高度)
            # 邊界框中心點
            cx, cy = bbox[0] + (bbox[2] // 2), \
                     bbox[1] + bbox[3] // 2

            poseInfo = {"lmList": mylmList, "bbox": bbox, "center": (cx, cy)}
            # 如果需要繪製
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS) # 繪製關鍵點和連接線
        if draw:
            return poseInfo, img # 返回姿勢資訊和繪製後的影像
        else:
            return poseInfo # 只返回姿勢資訊

    def findAngle(self, p1, p2, p3, img=None):
        """
        Finds angle between three landmark points.
        :param img: Image to draw output on.
        :param p1: Point1
        :param p2: Point2
        :param p3: Point3
        :param img: Image to draw output on.
        :return: Angle
                 Image with or without drawings
        """

        # Get the landmarks
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3
        # 使用 atan2 計算角度 (弧度制)，然後轉換為角度制
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                             math.atan2(y1 - y2, x1 - x2))
        # 處理超過 180° 的情況
        if angle < 0:
            angle += 360
        if angle > 180:
            angle = 360 - angle

        if img is not None: # 如果提供了影像
            # 在影像上繪製線條、圓點和角度值
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 10, (0, 255, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 255, 255), 2)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            return angle, img # 返回角度和繪製後的影像
        else:
            return angle # 只返回角度

    def findDistance(self, p1, p2, img=None):
        """
        Find the distance between two landmark points.
        :param p1: Point1
        :param p2: Point2
        :param img: Image to draw on.
        :return: Distance between the points
                 Line information
                 Image with output drawn                 
        """ 
        x1, y1 = p1
        x2, y2 = p2
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2 # 計算兩點的中點
        length = math.hypot(x2 - x1, y2 - y1) # 計算兩點間的距離
        info = [(x1, y1), (x2, y2), (cx, cy)] # 儲存相關點的資訊
        if img is not None:# 如果提供了影像
            # 在影像上繪製線條、圓點和距離值
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), 15, (0, 0, 255), cv2.FILLED)
            cv2.putText(img, str(int(length)), (cx - 50, cy + 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2) 
            return length, info, img # 返回距離、點資訊和繪製後的影像
        else:
            return length, info # 只返回距離和點資訊

    def angleCheck(self, myAngle, targetAngle, addOn=20):
        return targetAngle - addOn < myAngle < targetAngle + addOn


def main():
    cap = cv2.VideoCapture(0) # 開啟預設的網路攝影機 (通常索引為 0)
    detector = PoseDetector() # 建立 PoseDetector 物件，使用預設參數
    while True: # 不斷迴圈處理每一幀影像
        success, img = cap.read() # 從攝影機讀取一幀影像

        # 使用 detector 處理影像，進行姿勢偵測，並在影像上繪製結果
        # bboxWithHands=False 表示邊界框不特別考慮手部
        pose, img = detector.findPose(img, bboxWithHands=False)
        if pose: # 如果偵測到了姿勢 (pose 字典不是空的)
            center = pose["center"] # 獲取姿勢的中心點 (邊界框的中心)
            cv2.circle(img, center, 5, (255, 0, 255), cv2.FILLED) # 在中心點畫一個紫色的實心圓

        cv2.imshow("Image", img) # 顯示處理後的影像
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
