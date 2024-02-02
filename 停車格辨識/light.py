import cv2
import numpy as np

# 讀取影片
cap = cv2.VideoCapture("C:/Users/user/Desktop/parking/727509327.063853.mp4")

# 創建Lucas-Kanade光流法的參數
lk_params = dict(winSize=(15, 15),
                 maxLevel=2,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# 讀取第一幀
ret, old_frame = cap.read()
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)

# 將特徵點數據類型轉換為np.float32
p0 = np.float32(p0)

# 創建一個mask用於畫出光流
mask = np.zeros_like(old_frame)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 對影片進行處理灰度轉換
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 計算光流
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

    # 選取好的光流點
    good_new_int = np.int32(p1)
    good_old_int = np.int32(p0)

    # 畫出光流軌跡
    for i, (new, old) in enumerate(zip(good_new_int, good_old_int)):
        a, b = new.ravel()
        c, d = old.ravel()
        mask = cv2.line(mask, (a, b), (c, d), (0, 255, 0), 2)
        frame = cv2.circle(frame, (a, b), 5, (0, 0, 255), -1)

    # 合併原始影片和光流軌跡
    result = cv2.add(frame, mask)

    # 顯示處理後的影片
    cv2.imshow('Optical Flow', result)

    # 更新當前幀和特徵點
    old_gray = frame_gray.copy()
    p0 = p1.reshape(-1, 1, 2)

    # q退出
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
