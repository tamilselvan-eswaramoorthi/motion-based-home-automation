import numpy as np
import time
import urllib
import cv2
from PIL import Image
import serial
count = 0;

arduino = serial.Serial('/dev/ttyACM0', 9600)


fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 10.0, (640,480))

cap = cv2.VideoCapture(0)
interrupt=cv2.waitKey(10)
url='http://192.168.43.1:8080/shot.jpg'
fgbg = cv2.createBackgroundSubtractorMOG2()
b_imgResp = urllib.urlopen(url)
b_imgNp = np.array(bytearray(b_imgResp.read()),dtype=np.uint8)
b_img = cv2.imdecode(b_imgNp,-1)
b_img = cv2.resize(b_img, (640, 480)) 
b_img_1 = b_img[0:480, 320:640]
b_img_2 = b_img[0:480, 0:320]
while(1):
   
   imgResp = urllib.urlopen(url)
   imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
   img = cv2.imdecode(imgNp,-1)
   img = cv2.resize(img, (640, 480)) 
   img_1 = img[0:480, 320:640]
   cv2.imshow('1',img_1)
   img_2 = img[0:480, 0:320]
   cv2.imshow('2',img_2)
   cv2.imshow('Thres',img)
   out.write(img)
   k = cv2.waitKey(30) & 0xff
   
   if k == 27:
       break
    
   
   diff_1 = cv2.absdiff(b_img_1, img_1)
   mask = cv2.cvtColor(diff_1, cv2.COLOR_BGR2GRAY)

   r_thresh_frame_1 = cv2.threshold(diff_1, 30, 255, cv2.THRESH_BINARY)[1]
   r_thresh_frame_1 = cv2.dilate(r_thresh_frame_1, None, iterations = 2)   

   n_white_pix_1 = np.sum(r_thresh_frame_1 == 255)


   diff_2 = cv2.absdiff(b_img_2, img_2)
   mask = cv2.cvtColor(diff_2, cv2.COLOR_BGR2GRAY)

   r_thresh_frame_2 = cv2.threshold(diff_2, 30, 255, cv2.THRESH_BINARY)[1]
   r_thresh_frame_2 = cv2.dilate(r_thresh_frame_2, None, iterations = 2)   

   n_white_pix_2 = np.sum(r_thresh_frame_2 == 255)


   if n_white_pix_1 >= 35000 :
      print('yes for 1')
      arduino.write('H1') 

   else:
      print('no for 1')
      arduino.write('L1')

   if n_white_pix_2>= 35000 :
      print('yes for 2')
      arduino.write('H2') 


   else:
      print('no for 2')
      arduino.write('L2')


cap.release()
cv2.destroyAllWindows()
