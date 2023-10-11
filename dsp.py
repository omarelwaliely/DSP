import cv2
from skimage.metrics import structural_similarity as ssim

cap = cv2.VideoCapture('Video.mp4')

if not cap.isOpened():
    print("Error opening video stream or file")
    exit()

frame_rate = cap.get(cv2.CAP_PROP_FPS)  # Get the frame rate of the video
seconds = 1  # Number of seconds to check for repeated frames
frame_count = int(frame_rate * seconds)  # Calculate the number of frames in 'seconds'

ret, firstframe = cap.read()

if ret:
    count = 1  # Initialize count at 1 for the first frame
    while cap.isOpened():
        ret, frame = cap.read()

        if ret:
            similarity_index, _ = ssim(firstframe, frame, full=True)

            if similarity_index == 1.0:
                print(f"count: {count}, similarity: {similarity_index}")

            count += 1

            # If the count reaches the number of frames in 'seconds', reset the first frame
            if count > frame_count:
                count = 1
                firstframe = frame.copy()
        else:
            break

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
else:
    print("Error reading the first frame.")

cap.release()
cv2.destroyAllWindows()
