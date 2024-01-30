import cv2
import numpy as np

# 讀取影片
cap = cv2.VideoCapture("C:/Users/user/Desktop/parking/727509327.063853.mp4")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 將影片轉換為HSV色彩空間更容易捕捉顏色資訊
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 定義白色的HSV範圍 停車格是白色
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([255, 30, 255])
    #定義的上下界（lower_white 和 upper_white）
    #來創建一個二值化的遮罩（mask），將在這個範圍內的像素設為255，其他的設為0
    #這樣得到的遮罩即表示原始影像中屬於白色範圍的部分
    #這樣的二值化遮罩在後續的處理中可以用來標記或者過濾出白色的區域。

    # 根據HSV範圍過濾白色區域
    mask_white = cv2.inRange(hsv, lower_white, upper_white)

    # 進行形態學轉換來填充小的空洞，這裡使用開運算
    kernel = np.ones((5, 5), np.uint8)

    #用來消除白色區域中的小的空洞確保得到一個更連續的區域
    mask_white = cv2.morphologyEx(mask_white, cv2.MORPH_OPEN, kernel)

    # 在原始影片上標記白色區域
    result = cv2.bitwise_and(frame, frame, mask=mask_white)

    # 顯示處理後的影片
    cv2.imshow('Parking Lot Detection', result)

    # 'q' 鍵退出迴圈
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
