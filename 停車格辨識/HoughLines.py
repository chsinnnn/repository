import cv2
import numpy as np

# 讀取影片
cap = cv2.VideoCapture("C:/Users/user/Desktop/parking/727509324.994950.mp4")
ret, frame = cap.read()
# 成功讀取印true
print("Read frame successfully:", ret)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 對影片進行處理灰度轉換
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 使用霍夫變換來檢測直線
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=400)

    # 畫出檢測到的直線
    if lines is not None:
        for line in lines:  #遍歷檢測到的每條直線。
            rho, theta = line[0]  #轉換成直角座標的兩點 (x1, y1)(x2, y2)
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            #用來畫直線的起點。
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 *(-b))
            y2 = int(y0 - 1000 * (a))
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # 顯示處理後的影片
    cv2.imshow('Parking Lot Detection', frame)

    # 'q'退出迴圈 視窗關掉
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()