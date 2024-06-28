import cv2
import numpy as np
import joblib
from skimage.feature import local_binary_pattern
import pandas as pd
import time
import pi_servo_hat

def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        hsv_imagem = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        print(f'x = {x} e y = {y}')

def script(key, app):
    action = 0
    if key == ord('a'):
        action = 1
        app = "Relogio"
    elif key == ord('b'):
        action = 1
        app = "Definicoes"
    elif key == ord('c'):
        action = 1
        app = "Calculadora"
    elif key == ord('d'):
        action = 1
        app = "Internet"
    elif key == ord('e'):
        action = 1
        app = "Telefone"
    elif key == ord('f'):
        action = 1
        app = "S_Planner"
    elif key == ord('g'):
        action = 1
        app = "Email"
    elif key == ord('h'):
        action = 1
        app = "S_Voice"
    elif key == ord('i'):
        action = 1
        app = "Camara"
    elif key == ord('j'):
        action = 1
        app = "Contactos"
    elif key == ord('k'):
        action = 1
        app = "Galaxy_Store"
    elif key == ord('l'):
        action = 1
        app = "Radio"
    elif key == ord('m'):
        action = 1
        app = "Chrome"
    elif key == ord('n'):
        action = 1
        app = "Musica"
    elif key == ord('o'):
        action = 1
        app = "Galeria"
    elif key == ord('p'):
        action = 1
        app = "Gestor_Inteligente"
    elif key == ord('r'):
        action = 1
        app = "Ferramentas"
    elif key == ord('s'):
        action = 1
        app = "S_Health"
    elif key == ord('t'):
        action = 1
        app = "Video"
    elif key == ord('u'):
        action = 1
        app = "Mensagem"
    return app, action

def camera():
	ret, frame = cap.read()
	if ret:
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		ret, lower_thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_TOZERO)
		ret, upper_thresh = cv2.threshold(lower_thresh, 240, 255, cv2.THRESH_TOZERO_INV)
		ret, thresh = cv2.threshold(upper_thresh, 120, 255, cv2.THRESH_BINARY)
		cv2.imshow("frame", thresh)
		contours =  cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]
		bounding_boxes = []
		for i, contour in enumerate(contours):
			x, y, w, h = cv2.boundingRect(contour)
			if h > 80 and h < 120 and w > 80 and w < 120:
				cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
				bounding_boxes.append([x, y, w, h])
		return frame, bounding_boxes

def calcular_histograma_lbp(imagem, num_points, raio, metodo='uniform'):
	lbp = local_binary_pattern(imagem, num_points, raio, method=metodo)
	n_bins = int(lbp.max() + 1)
	hist, _ = np.histogram(lbp, bins=n_bins, range=(0, n_bins), density=True)
	return hist

def app_recognition(frame, bounding_boxes, app):
	bins, num_points, raio = 64, 64, 0.2
	
	hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	for i in range(len(bounding_boxes)):
		hsv_app = hsv_frame[bounding_boxes[i][1]:(bounding_boxes[i][1] + bounding_boxes[i][3]), bounding_boxes[i][0]:(bounding_boxes[i][0] + bounding_boxes[i][2])]
		H = cv2.calcHist([hsv_app], [0], None, [bins], [0, 256])
		S = cv2.calcHist([hsv_app], [1], None, [bins], [0, 256])
		V = cv2.calcHist([hsv_app], [2], None, [bins], [0, 256])
		gray_app = gray_frame[bounding_boxes[i][1]:(bounding_boxes[i][1] + bounding_boxes[i][3]), bounding_boxes[i][0]:(bounding_boxes[i][0] + bounding_boxes[i][2])]
		LBP = calcular_histograma_lbp(gray_app, num_points, raio)
		features = pd.DataFrame([np.concatenate([H.flatten(), S.flatten(), V.flatten(), LBP.flatten()])], columns=labels)
		if model.predict(features)[0] == app:
			app = i
			break
		else:
			pass
	return app

def arm_move(index, key):
    if key:
        if index == 12:
            robot.move_servo_position(0, 10, 90)
            time.sleep(1)
            robot.move_servo_position(1, 57.5, 90)
            time.sleep(2)
            robot.move_servo_position(3, -47, 90)
            time.sleep(0.2)
            robot.move_servo_position(3, -52, 90)
        elif index == 0:
            robot.move_servo_position(0, 17, 90)
            time.sleep(1)
            robot.move_servo_position(1, 61, 90)
            time.sleep(2)
            robot.move_servo_position(3, -45, 90)
            time.sleep(0.2)
            robot.move_servo_position(3, -52, 90)
        elif index == 9:
            robot.move_servo_position(0, 3.8, 90)
            time.sleep(1)
            robot.move_servo_position(3, -60, 90)
            time.sleep(1)
            robot.move_servo_position(2, -10, 90)
            time.sleep(1)
            robot.move_servo_position(1, 60, 90)
            time.sleep(2)
            robot.move_servo_position(3, -47, 90)
            time.sleep(0.2)
            robot.move_servo_position(3, -52, 90)
        time.sleep(1)
        robot.move_servo_position(0, 0, 90)
        time.sleep(1)
        robot.move_servo_position(1, 65, 90)
        time.sleep(1)
        robot.move_servo_position(2, -10, 90)
        time.sleep(1)
        robot.move_servo_position(3, -52, 90)

robot = pi_servo_hat.PiServoHat()
robot.set_pwm_frequency(50)
time.sleep(1)
robot.restart()
time.sleep(1)
robot.move_servo_position(0, 0, 90)
time.sleep(0.5)
robot.move_servo_position(1, 65, 90)
robot.move_servo_position(2, -10, 90)
robot.move_servo_position(3, -52, 90)

cap = cv2.VideoCapture(0)
model = joblib.load('/home/testing-robot/Downloads/Model.joblib')
cv2.namedWindow('frame')
cv2.setMouseCallback('frame', click_event)
aplicacao = "Chrome"

num_features = 64 + 1
labels = ([f'H{i}' for i in range(1, num_features)] + [f'S{i}' for i in range(1, num_features)] + [f'V{i}' for i in range(1, num_features)] + [f'LBP{i}' for i in range(1, num_features+2)])

while(True):
    pressedKey = cv2.waitKey(1) & 0xFF
    if pressedKey == ord('q'):
        print("Acabou")
        break
    aplicacao, pressedKey = script(pressedKey, aplicacao)
    frame, bboxes = camera()
    aplicacao = app_recognition(frame, bboxes, aplicacao)
    arm_move(aplicacao, pressedKey)
    
