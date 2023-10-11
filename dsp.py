import cv2
import numpy as np
from skimage.measure import compare_ssim as ssim

cap = cv2.VideoCapture('Video.mp4')
 
if (cap.isOpened()== False): 
  print("Error opening video stream or file")
firstret, firstframe = cap.read()
count =0
if firstret:
  while(cap.isOpened()):
    count+=1
    ret, frame = cap.read()
    if ret == True:
      if firstframe == frame:
        simlarityIndex = ssim(firstframe, frame)
        print(f"count:{count}, similarity: {simlarityIndex}")
      #cv2.imshow('Frame',frame)
      if cv2.waitKey(25) & 0xFF == ord('q'):
        break
    else: 
      break
cap.release()
cv2.destroyAllWindows()