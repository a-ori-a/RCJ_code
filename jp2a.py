import cv2
import image

HEIGHT = 36
chars = "   ..',;:ciodxkO0KXNWMMM%%%%"

cap = cv2.VideoCapture(0)
ret,frame = cap.read()

def pic2ascii(img):
    output = ''
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    for y in range(img.shape[0]-1): # 高さ
        for x in range(img.shape[1]-1):
            output += chars[int(img[x, y] / 255)]
        output += '\n'
    return output

print(pic2ascii(frame))