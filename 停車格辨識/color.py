import cv2
import numpy as np



# 定義鼠標事件的回調函數
def print_hsv(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        hsv_pixel = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        print(f"HSV value at ({x}, {y}): {hsv_pixel[y, x]}")

# 讀取照片
img = cv2.imread("C:/Users/user/Desktop/parking/S__74661918.jpg")


cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('Image', print_hsv)

# 調整視窗大小
cv2.resizeWindow('Image', 800, 600)

while True:
    
    cv2.imshow('Image', img)

    # 'q' 退出
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break


cv2.destroyAllWindows()