import cv2
import numpy as np
import pi_servo_hat
import time
import logging
#import matplotlib.pyplot as plt
#import time
#from .script1 import msg
#from inputimeout import inputimeout

logging.basicConfig(filename="Robot3.log", format='%(asctime)s %(message)s', filemode='w')
logger=logging.getLogger()
logger.setLevel(logging.DEBUG)

test = pi_servo_hat.PiServoHat()
# Set PWM Frequency to 50 Hz
test.set_pwm_frequency(200)
time.sleep(1)
test.restart()
time.sleep(1)
logger.info("Robot moves to default position")
test.move_servo_position(0, 0, 90)
time.sleep(1)
test.move_servo_position(1, 65, 90)
#time.sleep(1)
test.move_servo_position(2, -10, 90)
#time.sleep(1)
test.move_servo_position(3, -52, 90)
logger.info("Camera open")
cap = cv2.VideoCapture(0)
kernel = np.ones((4, 4), np.uint8)
a=1
ecra_desligado = 0
aplicacao = cv2.imread("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app2.png")


def click_event(event, x, y, flags, params):

    if event == cv2.EVENT_LBUTTONDOWN:
        hsv_imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)
        print(x)
        print(y)
        print(f'Cores do Ponto em BGR: {imagem[y, x]}')
        print(f'Cores do Ponto em HSV: {hsv_imagem[y, x]}')

""" def get_bboxes(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    median= cv2.medianBlur(blur, 3)
    ret, thresh_img = cv2.threshold(median, 160, 255, 0)
    thresh_img = cv2.morphologyEx(thresh_img, cv2.MORPH_GRADIENT, kernel)
    thresh_img = cv2.dilate(thresh_img, kernel, iterations = 5)
    contours =  cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]
    bounding_boxes = []
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        if h > 40 and h < 130 and w > 40 and w < 130:
            cv2.rectangle(frame, (x+w-80, y+h-100), (x + w, y + h), (0, 255, 0), 1) 
            row = [x, y, w, h]
            bounding_boxes.append(row)
    #    if bounding_boxes.shape[0] == 2:
    #        global ecra_desligado
    #        ecra_desligado = 1
    #        return frame
    #if a==1:
    #    print(bounding_boxes)
    bounding_boxes = np.asarray(bounding_boxes)
    return frame, bounding_boxes """

def get_bboxes(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (131, 131), 0)#161.31.21
    median= cv2.medianBlur(blur, 27)
    ret, thresh_img = cv2.threshold(median, 160, 255, 0)
    thresh_img = cv2.morphologyEx(thresh_img, cv2.MORPH_GRADIENT, kernel)
    thresh_img = cv2.dilate(thresh_img, kernel, iterations = 21)
    contours =  cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]
    #cv2.imshow('frame2', thresh_img)
    bounding_boxes = []
    somaw = 0
    somah = 0
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        if h > 30 and h < 300 and w > 30 and w < 300:
            bounding_boxes.append([x, y, w, h])
            somaw += w
            somah += h
    #    if bounding_boxes.shape[0] == 2:
    #        global ecra_desligado
    #        ecra_desligado = 1
    #        return frame
    bounding_boxes = np.asarray(bounding_boxes)
    #for i in range(bounding_boxes.shape[0]):
    #    cv2.rectangle(frame, (bounding_boxes[i, 0], bounding_boxes[i, 1]), (bounding_boxes[i, 0] + bounding_boxes[i, 2], bounding_boxes[i,1] + bounding_boxes[i, 3]), (0, 255, 0), 1)
    #Ajustar y
    i=0
    while i < bounding_boxes.shape[0]:
        num, pos = 0, 0
        for j in range(bounding_boxes.shape[0]):
            if (bounding_boxes[i, 1] - 80) < bounding_boxes[j, 1] < (bounding_boxes[i, 1] + 80):
                num += 1
                pos += bounding_boxes[j, 1]
        for j in range(i, i + num):
            try :
                bounding_boxes[j, 1] = pos/num
            except:
                pass
        i += num
    #Ajustar o x e a largura e altura das bboxes (w, h)
    for i in range(bounding_boxes.shape[0]):

        #Este é para o x (Nao está 100% correto - Podemos melhorar algoritmo)
        num, pos = 0, 0
        for j in range(bounding_boxes.shape[0]):
            if (bounding_boxes[i, 0] - 80) < bounding_boxes[j, 0] < (bounding_boxes[i, 0] + 80):
                num += 1
                pos += bounding_boxes[j, 0]
        for j in range(bounding_boxes.shape[0]):
            if (bounding_boxes[i, 0] - 80) < (pos/num) < (bounding_boxes[i, 0] + 80):
                bounding_boxes[i, 0] = pos/num

        #Mesmo tamanho para bboxes
        bounding_boxes[i, 2] = somaw/bounding_boxes.shape[0]
        bounding_boxes[i, 3] = somah/bounding_boxes.shape[0]
        #cv2.rectangle(frame, (bounding_boxes[i, 0], bounding_boxes[i, 1]), (bounding_boxes[i, 0] + bounding_boxes[i, 2], bounding_boxes[i,1] + bounding_boxes[i, 3]), (0, 255, 0), 1)
    #Ordenar Bboxes
    try:
        bounding_boxes = bounding_boxes[np.lexsort((bounding_boxes[:, 0], bounding_boxes[:, 1]))]
    except:
        print("No bounding boxes")

    for i in range(bounding_boxes.shape[0]):
        cv2.rectangle(frame, (bounding_boxes[i, 0], bounding_boxes[i, 1]), (bounding_boxes[i, 0] + bounding_boxes[i, 2], bounding_boxes[i,1] + bounding_boxes[i, 3]), (0, 255, 0), 1)
    return frame, bounding_boxes

def app_recognition(app, frame_bbox, bounding_boxes):
    MSE_error = np.zeros(((bounding_boxes.shape[0]), 1))
    for i in range(bounding_boxes.shape[0]):
        a = bounding_boxes[i, 0]
        b = a + bounding_boxes[i, 2]
        c = bounding_boxes[i, 1]
        d = c + bounding_boxes[i, 3]
        
        """#Código para recolha de dados
        if i==0:
            cv2.imwrite("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app0.png", frame_bbox[c:d, a:b])
        if i==1:
            cv2.imwrite("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app1.png", frame_bbox[c:d, a:b])
        if i==2:
            cv2.imwrite("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app2.png", frame_bbox[c:d, a:b])
        if i==3:
            cv2.imwrite("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app3.png", frame_bbox[c:d, a:b])
        if i==4:
            cv2.imwrite("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app4.png", frame_bbox[c:d, a:b])
        if i==5:
            cv2.imwrite("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app5.png", frame_bbox[c:d, a:b])
        if i==6:
            cv2.imwrite("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app6.png", frame_bbox[c:d, a:b])
        if i==7:
            cv2.imwrite("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app7.png", frame_bbox[c:d, a:b])
        if i==8:
            cv2.imwrite("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app8.png", frame_bbox[c:d, a:b])
        if i==9:
            cv2.imwrite("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app9.png", frame_bbox[c:d, a:b])
        if i==10:
            cv2.imwrite("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app10.png", frame_bbox[c:d, a:b])
        if i==11:
            cv2.imwrite("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app11.png", frame_bbox[c:d, a:b])
        if i==12:
            cv2.imwrite("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app12.png", frame_bbox[c:d, a:b])
        if i==13:
            cv2.imwrite("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app13.png", frame_bbox[c:d, a:b])
        if i==14:
            cv2.imwrite("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app14.png", frame_bbox[c:d, a:b])
        if i==15:
            cv2.imwrite("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app15.png", frame_bbox[c:d, a:b])
        if i==16:
            cv2.imwrite("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app16.png", frame_bbox[c:d, a:b])
        if i==17:
            cv2.imwrite("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app17.png", frame_bbox[c:d, a:b])
        if i==18:
            cv2.imwrite("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app18.png", frame_bbox[c:d, a:b])
        if i==19:
            cv2.imwrite("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app19.png", frame_bbox[c:d, a:b])"""

        img3 = frame_bbox[c:d, a:b]
        
        app = cv2.resize(app, (img3.shape[1], img3.shape[0]))
        MSE_error[i] = ((app-img3)**2).mean(axis=None)

    least_MSE = np.argmin(MSE_error)
    a = bounding_boxes[least_MSE,0]
    b = a + bounding_boxes[least_MSE,2]
    c = bounding_boxes[least_MSE,1] 
    d = c + bounding_boxes[least_MSE,3]
    img3 = frame_bbox[c:d, a:b]
    cv2.imshow('frame2', img3)
    cv2.imshow('frame', frame_bbox)
    return bounding_boxes[least_MSE, :]

def camera(app, key):
    ret, frame = cap.read()
    if key:
        logger.info("Processing image")
    if ret:
        frame_bbox, bounding_boxes = get_bboxes(frame)
        #print(bounding_boxes)
    if key:
        logger.info("Image with bounding boxes")
    app = app_recognition(app, frame_bbox, bounding_boxes)
    if key:
        logger.info("App Location detected")
    #if app != 'rui':
    arm_move(bounding_boxes, app, key)
    """else:
        print("Going back to main menu")
        test.move_servo_position(0, 20, 90)
        time.sleep(1)
        test.move_servo_position(1, 60, 90)
        time.sleep(0.5)
        test.move_servo_position(1, 57.5, 90)
        time.sleep(0.5)
        test.move_servo_position(1, 55, 90)
        time.sleep(1)
        test.move_servo_position(3, -45, 90)
        time.sleep(1)
        test.move_servo_position(2, 0, 90)
        time.sleep(1)
        test.move_servo_position(3, -42, 90)
        time.sleep(1)
        test.move_servo_position(3, -45, 90)"""
    return frame#_bbox#, bounding_boxes

def script(key, app):
    action = 0
    if key == ord('a'):
        action = 1
        logger.info("Clock app selected")
        app = cv2.imread("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app0.png")
        print("Relógio")
    elif key == ord('b'):
        action = 1
        app = cv2.imread("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app1.png")
        print("Definições")
    elif key == ord('c'):
        action = 1
        app = cv2.imread("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app2.png")
        print("Calculadora")
    elif key == ord('d'):
        action = 1
        app = cv2.imread("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app3.png")
        print("Internet")
    elif key == ord('e'):
        action = 1
        app = cv2.imread("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app4.png")
        print("Chamadas")
    elif key == ord('f'):
        action = 1
        app = cv2.imread("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app5.png")
        print("Calendário")
    elif key == ord('h'):
        action = 1
        app = cv2.imread("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app6.png")
        print("E-mail")
    elif key == ord('i'):
        action = 1
        app = cv2.imread("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app7.png")
        print("S Voice")
    elif key == ord('j'):
        action = 1
        app = cv2.imread("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app8.png")
        print("Camera")
    elif key == ord('k'):
        action = 1
        app = cv2.imread("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app9.png")
        logger.info("Contact List app selected")
        print("Contactos")
    elif key == ord('l'):
        action = 1
        app = cv2.imread("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app10.png")
        print("Galaxy Store")
    elif key == ord('m'):
        action = 1
        app = cv2.imread("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app11.png")
        print("Rádio")
    elif key == ord('n'):
        action = 1
        logger.info("Google Chrome selected")
        app = cv2.imread("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app12.png")
        print("Google Chrome")
    elif key == ord('o'):
        action = 1
        app = cv2.imread("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app13.png")
        print("Música")
    elif key == ord('p'):
        action = 1
        app = cv2.imread("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app14.png")
        print("Galeria")
    elif key == ord('r'):
        action = 1
        app = cv2.imread("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app15.png")
        print("Gestor Inteligente")
    elif key == ord('s'):
        action = 1
        app = cv2.imread("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app16.png")
        print("Pasta")
    elif key == ord('t'):
        action = 1
        app = cv2.imread("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app17.png")
        print("S Health")
    elif key == ord('u'):
        action = 1
        app = cv2.imread("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app18.png")
        print("Video")
    elif key == ord('v'):
        action = 1
        app = cv2.imread("/home/testing-robot/Cap_Project/Python/Datasets/Page 1/Cam_Ric/app19.png")
        print("Mensagem")
    return app, action

def arm_move(bounding_boxes, app, key):
    if key:
        time.sleep(3)
        index = 0
        for i in range(bounding_boxes.shape[0]):
            if (bounding_boxes[i] == app).all():
                index = i
                break
        
        #Movimento do Braço conforme tecla - Supõe que as apps estão todas! E supõe que o tele está sempre no mesmo sítio
        #Não faz posição zerozero e não faz posição zero. Isto garantia qualquer tela e qualquer posição do tele.
        if index == 12:
            logger.info("Robot moving to Google Chrome app")
            test.move_servo_position(0, 10, 90)
            time.sleep(1)
            test.move_servo_position(1, 57.5, 90)
            time.sleep(2)
            test.move_servo_position(3, -47, 90)
            time.sleep(0.2)
            test.move_servo_position(3, -52, 90)
        elif index == 0:
            logger.info("Robot moving to Clock app")
            test.move_servo_position(0, 17, 90)
            time.sleep(1)
            test.move_servo_position(1, 61, 90)
            time.sleep(2)
            test.move_servo_position(3, -45, 90)
            time.sleep(0.2)
            test.move_servo_position(3, -52, 90)
        elif index == 9:
            logger.info("Robot moving to Contact List app")
            test.move_servo_position(0, 3.8, 90)
            time.sleep(1)
            test.move_servo_position(3, -60, 90)
            time.sleep(1)
            test.move_servo_position(2, -10, 90)
            time.sleep(1)
            test.move_servo_position(1, 60, 90)
            time.sleep(2)
            test.move_servo_position(3, -47, 90)
            time.sleep(0.2)
            test.move_servo_position(3, -52, 90)
        logger.info("Robot moves back to default position")
        time.sleep(1)
        test.move_servo_position(0, 0, 90)
        time.sleep(1)
        test.move_servo_position(1, 65, 90)
        time.sleep(1)
        test.move_servo_position(2, -10, 90)
        time.sleep(1)
        test.move_servo_position(3, -52, 90)
        time.sleep(1)

cv2.namedWindow('frame')
cv2.setMouseCallback('frame', click_event)
z=0
while(True):
    pressedKey = cv2.waitKey(1) & 0xFF
    if pressedKey == ord('q'):
        logger.info("Exiting program")
        print("Acabou")
        break
    aplicacao, pressedKey = script(pressedKey, aplicacao)
    imagem = camera(aplicacao, pressedKey)
    #cv2.imshow("frame", imagem)
    """ a=0
    if ecra_desligado:
        print("Ecrã desligado") 
        break """

    

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
