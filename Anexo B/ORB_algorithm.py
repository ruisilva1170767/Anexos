import cv2
import numpy as np

cap = cv2.VideoCapture(0)
img1 = cv2.imread("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app2.png")
#img1 = cv2.imread("/home/testing-robot/Cap_Project/Python/tenta.png")
orb = cv2.ORB_create(nfeatures=3000)

def click_event(event, x, y, flags, params):

    if event == cv2.EVENT_LBUTTONDOWN:
        hsv_imagem = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
        print(x)
        print(y)
        print(f'Cores do Ponto em BGR: {img2[y, x]}')
        print(f'Cores do Ponto em HSV: {hsv_imagem[y, x]}')
cv2.namedWindow('Img2')
cv2.setMouseCallback('Img2', click_event)
cv2.namedWindow('Img3')

while True:
	ret, img2 = cap.read()
	#img2 = img2[214:292, 1228:1318]
	if ret:
		kp1, des1 = orb.detectAndCompute(img1, None)
		kp2, des2 = orb.detectAndCompute(img2, None)
		
		bf = cv2.BFMatcher(cv2.NORM_L2SQR, crossCheck=True)
		matches = bf.match(des1, des2)
		matches = sorted(matches, key=lambda x:x.distance)
		
		img3 = cv2.drawMatches(img1, kp1, img2, kp2, matches, img2, None)
		width = int(img3.shape[1]*0.6)
		height = int(img3.shape[0]*0.6)
		dim = (width, height)
		img3 = cv2.resize(img3, dim)
		cv2.imshow("Img1", img1)
		cv2.imshow("Img2", img2)
		cv2.imshow("Img3", img3)
		cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()
