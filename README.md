# 健身動作偵測計數器

![image](https://github.com/Weber0531/MediaPipe/blob/main/demo/Education/demo.gif)

這是一個使用 Python、OpenCV 與 MediaPipe 製作的健身動作偵測程式，能即時透過攝影機辨識角度，自動計數並提供中文鼓勵提示。

---

## 🎯 功能介紹

- ✅ 使用 MediaPipe 偵測人體姿勢關節（Pose）
- ✅ 即時追蹤角度並視覺化
- ✅ 自動記錄次數
- ✅ 顯示「中文提示文字」鼓勵使用者
- ✅ 使用 PIL 處理中文文字，支援繁體字型

---

## 🚀 安裝與執行方式

### 1️⃣ clone本專案
```bash
git clone https://github.com/a0978314359-afk/project000.git
```

### 2️⃣ 移動到專案內
```bash
cd project000/
```

### 3️⃣ 安裝套件

請先安裝必要的 Python 套件

```bash
pip install opencv-python mediapipe Pillow numpy
```

### 4️⃣ 執行主程式(biceps.py為例)
```bash
cd Education/
python3 biceps.py
```
