import cv2
import numpy as np

# 讀取照片
img = cv2.imread("C:/Users/user/Desktop/parking/S__74661918.jpg")

# 對照片進行灰度轉換
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 使用霍夫變換來檢測直線
edges = cv2.Canny(gray, 50, 150, apertureSize=3)
lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=600)

# 畫出檢測到的直線
if lines is not None:
    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

# 調整顯示的大小
resized_img = cv2.resize(img, (img.shape[1] // 2, img.shape[0] // 2))

# 顯示處理後的照片
cv2.imshow('Parking Lot Detection', resized_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
