import cv2
import pickle
from rotaParking import recRota

filepath = r'C:\opencv\parking.jpg'
filename = 'parking_position.txt'
w, h = 120, 160

try:
    with open(filename, 'rb') as file_object:
        posList = pickle.load(file_object)
except:
    posList = []

def onMouse(events, x, y, flag, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for index, pos in enumerate(posList):
            if pos[0] < x < pos[0] + w and pos[1] < y < pos[1] + h:
                posList.pop(index)
    with open(filename, 'wb') as file_object:
        pickle.dump(posList, file_object)

# 提前創建可調整大小的窗口
cv2.namedWindow('img', cv2.WINDOW_NORMAL)

# 在創建窗口後，再設置滑鼠回調函數
cv2.setMouseCallback('img', onMouse)

while True:
    img = cv2.imread(filepath)
    for pos in posList:
        img, angle = recRota(img, pos[0], pos[1], pos[0], pos[1], w, h, -4)

    cv2.imshow('img', img)
    key = cv2.waitKey(0)
    cv2.destroyAllWindows()
    break
