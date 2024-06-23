import cv2

cap=cv2.VideoCapture(0)
i=0

while (i < 101):
	ret, frame = cap.read()
	cv2.imshow("frame",frame) 
	if cv2.waitKey(1) & 0xFF == ord('s'):
		cv2.imwrite(f"/home/testing-robot/Cap_Project/Python/Datasets/Camera_Dataset/imagem{i}.png", frame)
		i += 1
	else:
		continue