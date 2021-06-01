###################################
# make frame image to numpy array #
###################################

import cv2
import numpy as np

def frame_npArray():
    cap = cv2.VideoCapture(0)
    np_framelist = []

    while cap.isOpened():
        ret, frame = cap.read()
        np_frame = np.array(frame)
        np_framelist.append(np_frame)

        cv2.imshow('Raw Webcam Feed', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    np_framelist = np.array(np_framelist)
    print("np_framelist.shape")
    print(np_framelist.shape)
    print("*********************************************************")
    print(np_framelist)

    cap.release()
    cv2.destroyAllWindows()

    

if __name__ == "__main__":
    frame_npArray()
