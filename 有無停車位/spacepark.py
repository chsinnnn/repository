import cv2 
import pickle 
import numpy as np 
from rotaParking import recRota # 導入自定義的旋轉矩形框函數 
from rotaParking import drawLine # 導入繪製旋轉矩形線條函數

#（1）讀取視頻 
filepath = r'C:\opencv\parking.mp4' 
cap = cv2.VideoCapture(filepath)

# 初始的車位框顏色 
color = (255,255,0)

#（2）導入先前記錄下來的車位矩形框的左上角坐標 
filename = 'parking_position.txt' # 保存的車位坐標
with open(filename, 'rb') as f: 
    posList = pickle.load(f)

#（3）處理每一幀圖像 
while True: 
    # 記錄有幾個空車位
    spacePark = 0 
    # 返回圖像是否讀取成功，以及讀取的幀圖像img 
    success, img = cap.read() 
    # 為了使裁剪後的單個車位裡面沒有繪製的邊框，需要在畫車位框之前，把原圖像複製一份 
    imgCopy = img.copy()
    # 獲得整每幀圖片的寬和高 
    img_w, img_h = img.shape[:2] #shape是(w,h,c) 
    # ==1== 轉換灰度圖，通過形態學處理來檢測車位內有沒有車 
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    # ==2== 高斯濾波,卷積核3*3,沿x和y方向的卷積核的標準差為1 
    imgGray = cv2.GaussianBlur(imgGray, (3,3), 1) 
    # ==3== 二值圖，自適應閾值方法 
    imgThresh = cv2.adaptiveThreshold(imgGray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 101, 20) 
    # ==4== 刪除零散的白點，如果車位上有車，那麼車位上的像素數量(白點)很多，如果沒有車，車位框內基本沒什麼白點 
    imgMedian = cv2.medianBlur(imgThresh, 5) 
    # ==5== 擴張白色部分，膨脹 
    kernel = np.ones((3,3), np.uint8) # 設置卷積核 
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1) # 疊代次數為1 
    # 由於這個視頻比較短，就循環播放這個視頻 
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT): 
        # 如果當前幀==總幀數，那就重置當前幀為0 
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    #（4）繪製停車線矩形框 
    w, h = 90, 160 # 矩形框的寬和高 
    # 遍歷所有的矩形框坐標 
    for pos in posList: 
        # 得到旋轉後的矩形的四個角坐標，傳入原圖，旋轉參考點坐標，矩形框左上角坐標，框的寬w和高h，逆時針轉4° 
        angle = recRota(imgDilate, pos[0], pos[1], pos[0], pos[1], w, h, -4, draw=False) # 裁剪的車位不繪製車位圖 
        #（5）裁剪所有的車位框，由於我們的矩形是傾斜的，先要把矩形轉正之後再裁剪 
        # # 變換矩陣，以每個矩形框的左上坐標為參考點，順時針尋轉4°，旋轉後的圖像大小不變 
        rota_params = cv2.getRotationMatrix2D(angle[0], angle=-4, scale=1)
        # 旋轉整張幀圖片，輸入img圖像，變換矩陣，指定輸出圖像大小 
        rota_img = cv2.warpAffine(imgDilate, rota_params, (img_w, img_h))
        # 裁剪擺正了的矩形框，先指定高h，再指定寬w 
        imgCrop = rota_img[pos[1]:pos[1]+h, pos[0]:pos[0]+w] 
        # 顯示裁剪出的圖像 
        cv2.imshow('imgCrop', imgCrop) 
        #（6）計算每個裁剪出的單個車位有多少個像素點 
        count = cv2.countNonZero(imgCrop) 
        # 將計數顯示在矩形框上 
        cv2.putText(imgCopy, str(count), (pos[0]+5, pos[1]+20), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0,255,255), 2)
        #（7）確定車位上是否有車 
        if count < 3000: # 像素數量小於2500輛就是沒有車 
            color = (0,255,0) # 沒有車的話車位線就是綠色 
            spacePark += 1 # 每檢測到一個空車位，數量就加一 
        else: color = (0,0,255) # 有車時車位線就是紅色 
        #（8）繪製所有車位的矩形框 
        # 在複製後的圖像上繪製車位框 
        imgCopy = drawLine(imgCopy, angle, color, 3)
    # 繪製目前還剩餘幾個空車位 
    cv2.rectangle(imgCopy, (0,150), (200,210), (255,255,0), cv2.FILLED) 
    cv2.rectangle(imgCopy, (5,155), (195,205), (255,255,255), 3) 
    cv2.putText(imgCopy, 'FREE: '+str(spacePark), (31,191), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,255), 3) 
    #（9）顯示圖像，輸入窗口名及圖像數據 
    cv2.imshow('img', imgCopy) # 原圖 
    cv2.imshow('imgGray', imgGray) # 高斯濾波後 
    cv2.imshow('imgThresh', imgThresh) # 二值化後 
    cv2.imshow('imgMedian', imgMedian) # 模糊後 
    cv2.imshow('imgDilate', imgDilate) # 膨脹 
    
    if cv2.waitKey(1) & 0xFF==27: #每幀滯留20毫秒後消失，ESC鍵退出
        break 
# 釋放視頻資源 
cap.release() 
cv2.destroyAllWindows()
