import cv2
import numpy as np

def resampleVideo(input, output, skipframe):
    cap = cv2.VideoCapture(input)

    if not cap.isOpened():
        print("Error opening video stream or file")
        return

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output, fourcc, fps, (width, height))

    count = 0
    while True:
        ret, frame = cap.read()

        if not ret:
            break

        if count % (skipframe+1) == 0:
            out.write(frame)

        count += 1
    cap.release()
    out.release()

    print(f"Resampled video saved as '{output}'")

def mse(fr1, fr2,w,h):
   diff = cv2.subtract(fr1, fr2)
   err = np.sum(diff**2)
   mse = err/(float(w*h))
   return mse

def findPeriod(input):
    cap = cv2.VideoCapture(input)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        count += 1
        if count == 300: #choosing a random sample frame. Made it high so we can skip the beginning black screen portion
            checkframe = frame
        elif count > 300:
            currmse = mse(frame,checkframe,width,height)
            if currmse < 60: #chose a threshold of 60, based on printing, it seemed that most frames had a difference of around 100 showing they are different
                return count - 300 #period is the sample - the current frame
        
    cap.release()

input = 'Video.mp4'
period = findPeriod(input) #the skip are the frames in between the period so if 1 and 4 are the a repeat, period is 4 but skip is 3 frames
skip = period -1 #the skip are the frames in between the period so if 1 and 4 are the a repeat, period is 4 but skip is 3 frames
print(skip)
resampleVideo(input, 'skiptwo.mp4', 2)
resampleVideo(input, 'Output1.mp4', skip)
resampleVideo(input, 'Output2.mp4', period + 1)