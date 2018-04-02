import numpy as np
import time
import urllib
import cv2
from PIL import Image
import serial
count = 0;

arduino = serial.Serial('/dev/ttyACM0', 9600)
#  ser = serial.Serial('/dev/tty.usbserial', 9600)
start_row, start_col = int(0), int(0)


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
b_thresh_frame = cv2.threshold(b_img, 30, 255, cv2.THRESH_BINARY)[1]
b_thresh_frame = cv2.dilate(b_thresh_frame, None, iterations = 2)
b_gray_image = cv2.cvtColor(b_img, cv2.COLOR_BGR2GRAY)
ret,b_thresh_img = cv2.threshold(b_gray_image,127,255,cv2.THRESH_BINARY)
#cv2.imshow('d',b_img)


height, width = b_img.shape[:2]
print b_img.shape

while(1):
   
   imgResp = urllib.urlopen(url)
   imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
   img = cv2.imdecode(imgNp,-1)
   img = cv2.resize(img, (640, 480)) 

   fgmask = fgbg.apply(img)

   thresh_frame = cv2.threshold(fgmask, 30, 255, cv2.THRESH_BINARY)[1]
   thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)
   cv2.imshow('Thres',img)
   out.write(img)
   k = cv2.waitKey(30) & 0xff
   
   if k == 27:
       break
    
   
   diff = cv2.absdiff(b_img, img)
   mask = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

   r_thresh_frame = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)[1]
   r_thresh_frame = cv2.dilate(r_thresh_frame, None, iterations = 2)   
 #  cv2.imshow('Thres',r_thresh_frame)   
   #if np.sum(r_thresh_frame == 255) - np.sum(b_thresh_img == 255)>=1000 :
      
      # b_imgResp = urllib.urlopen(url)
      # b_imgNp = np.array(bytearray(b_imgResp.read()),dtype=np.uint8)
      # b_img = cv2.imdecode(b_imgNp,-1)
      # b_img = cv2.resize(b_img, (640, 480)) 
      # b_thresh_frame = cv2.threshold(b_img, 30, 255, cv2.THRESH_BINARY)[1]
      # b_thresh_frame = cv2.dilate(b_thresh_frame, None, iterations = 2)
      # gray_image = cv2.cvtColor(b_img, cv2.COLOR_BGR2GRAY)
      # ret,thresh_img = cv2.threshold(gray_image,127,255,cv2.THRESH_BINARY)
      # cv2.imshow('dddddddddd',thresh_img)
      # print('f')
   #print(np.sum(r_thresh_frame == 255))
   n_white_pix = np.sum(r_thresh_frame == 255)
   #print(n_white_pix)
   if n_white_pix >= 35000 :

      print('yes')
 
      arduino.write('H') 
      # ser.write(b'1') 

   else:
      print('no')

      arduino.write('L')
      # ser.write(b'0') 

cap.release()
cv2.destroyAllWindows()
