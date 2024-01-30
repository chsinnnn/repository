import cv2
import numpy as np

# 讀取圖片
img = cv2.imread("C:/Users/user/Desktop/parking/S__147496983.jpg")

# 將圖片轉換為HSV色彩空間
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# 定義白色的HSV範圍
lower_white = np.array([0, 0, 200])
upper_white = np.array([255, 30, 255])

# 根據HSV範圍過濾白色區域
mask_white = cv2.inRange(hsv, lower_white, upper_white)

# 進行形態學轉換來填充小的空洞，這裡使用開運算
kernel = np.ones((5, 5), np.uint8)
mask_white = cv2.morphologyEx(mask_white, cv2.MORPH_OPEN, kernel)

# 在原始影片上標記白色區域
result = cv2.bitwise_and(img, img, mask=mask_white)

# 顯示處理後的影片
cv2.imshow('Parking Lot Detection', result)

# 'q' 退出迴圈
cv2.waitKey(0)

# 釋放資源
cv2.destroyAllWindows()
