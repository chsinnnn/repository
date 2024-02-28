# 矩形框順時針旋轉
import cv2 
import math

# 傳入旋轉的參考點坐標，矩形框左上角坐標(x,y)，框的寬w和高h，旋轉角度a
def angleRota(center_x, center_y, x, y, w, h, a):

    # 角度轉弧度
    a = (math.pi/180)*a
    # 旋轉前左上角坐標
    x1, y1 = x, y
    # 右上角坐標
    x2, y2 = x+w, y
    # 右下角坐標
    x3, y3 = x+w, y+h
    # 左下角坐標
    x4, y4 = x, y+h
    # 像素坐標是整數
    
    # 旋轉後的左上角坐標
    px1 = int((x1 - center_x) * math.cos(a) - (y1 - center_y) * math.sin(a) + center_x)
    py1 = int((x1 - center_x) * math.sin(a) + (y1 - center_y) * math.cos(a) + center_y) 
    # 右上角坐標 
    px2 = int((x2 - center_x) * math.cos(a) - (y2 - center_y) * math.sin(a) + center_x) 
    py2 = int((x2 - center_x) * math.sin(a) + (y2 - center_y) * math.cos(a) + center_y) 
    # 右下角坐標 
    px3 = int((x3 - center_x) * math.cos(a) - (y3 - center_y) * math.sin(a) + center_x) 
    py3 = int((x3 - center_x) * math.sin(a) + (y3 - center_y) * math.cos(a) + center_y) 
    # 左下角坐標 
    px4 = int((x4 - center_x) * math.cos(a) - (y4 - center_y) * math.sin(a) + center_x) 
    py4 = int((x4 - center_x) * math.sin(a) + (y4 - center_y) * math.cos(a) + center_y)

    # 保存每一個角的坐標
    pt1 = (px1, py1) 
    pt2 = (px2, py2) 
    pt3 = (px3, py3) 
    pt4 = (px4, py4)

    # 存儲每個角的坐標 
    angle = [pt1, pt2, pt3, pt4]

    # 返回調整後的坐標 
    return angle

# 繪製旋轉後的矩形框 
def drawLine(img, angle, color, thickness): 
    
    # 分別繪製四條邊 
    cv2.line(img, angle[0], angle[1], color, thickness) 
    cv2.line(img, angle[1], angle[2], color, thickness) 
    cv2.line(img, angle[2], angle[3], color, thickness) 
    cv2.line(img, angle[3], angle[0], color, thickness) 
    
    # 返回繪製好旋轉矩形的圖像
    return img

# 矩形旋轉 
def recRota(img, center_x, center_y, x1, y1, w, h, rota, draw=True): 
    ''' img: 原圖像
    (center_X, center_y): 旋轉參考點的坐標 
    (x1, y1): 矩形框左上角坐標 
    w: 矩形框的寬 
    h: 矩形框的高 
    rota: 順時針的旋轉角度,如:30° 
    ''' 
    color = (255,255,0) # 繪製停車線的線條顏色 
    thickness = 2 # 停車線線條寬度 
    
    #（1）計算旋轉一定角度後的四個角的坐標 
    angle = angleRota(x1, y1, x1, y1, w, h, rota) 
    
    #（2）繪製旋轉後的矩形 
    if draw == True: 
        img = drawLine(img, angle, color, thickness) 
        # 返回繪製後的圖像，以及矩形框的四個角的坐標 
        return img, angle 
    else: 
        return angle
