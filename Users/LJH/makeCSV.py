from cv2 import data
import fileControlModule as fcm
import mediapipe as mp
import pandas as pd
import numpy as np
import cv2
import csv
import os

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic


Path = os.getcwd()                          # 현재 작업이 실행되고 있는 디렉토리
dataPath = f'{Path}/{"Users/LJH/data"}'     # 데이터가 저장되어 있는 폴더 
categories = os.listdir(dataPath)           # 분류된 폴더명 저장 즉, 카테고리는 == 클래스 이름
categories.remove(".DS_Store")              # .DS_Store 파일 리스트에서 삭제 (맥 전용)

filepath_list = []                          #파일 경로 저장 리스트, 실질적으로 영상을 열기위한 경로로 사용
class_size_list = []                        #각 클래스별 파일(영상) 개수
category = []

fc = fcm.fileControl()

categorie_files = len(categories)
for i in range(categorie_files):
    if category == []:
        category.append(categories[i])
    else:
        category.clear()
        category.append(categories[i])

    categories_path = fc.chooseGesture(dataPath, i)   #의미로 넘버링된 동영상 폴더 접근
    categories_list = os.listdir(categories_path)

    if ".DS_Store" in categories_list:
        categories_list.remove(".DS_Store") 

    class_size_list.append(len(categories_list)) #각 클래스별 파일 수 저장
    
    for j, file in enumerate(categories_list):
        filepath = fc.chooseFile(categories_path, j)   #동영상 하나하나의 경로 지정
        filepath_list.append(filepath)    #리스트에 동영상 경로 저장

################################################################

cap = cv2.VideoCapture(filepath_list[0])
framecount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(framecount)

################################################################
# Initiate holistic model
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    framelist = []
    while cap.isOpened():
        ret, frame = cap.read()
        
        try:
            #RGB로 변환
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
        except:
            break
        
        #특징점 이미지에 나타내기
        results = holistic.process(image)
        
        #렌더링을 위해서 이미지 다시 BGR로 변환
        image.flags.writeable = True   
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # 1. Draw face landmarks
        mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACE_CONNECTIONS, 
                                 mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1),
                                 mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
                                 )
        
        # 2. Right hand
        mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                                 mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4),
                                 mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2)
                                 )

        # 3. Left Hand
        mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                                 mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4),
                                 mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2)
                                 )

        # 4. Pose Detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS, 
                                 mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4),
                                 mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                                 )

        cv2.imshow('Raw Webcam Feed', image)

        image_height, image_width, _ = image.shape

        face = results.face_landmarks.landmark
        face_row = list(np.array([[landmark.x * image_height, landmark.y * image_height] for landmark in face]).flatten())

        pose = results.pose_landmarks.landmark
        pose_row = list(np.array([[landmark.x * image_height, landmark.y * image_height] for landmark in pose]).flatten())

        try:
            left_hand = results.left_hand_landmarks.landmark
            left_hand_row = list(np.array([[landmark.x * image_height, landmark.y * image_height] for landmark in left_hand]).flatten())
        except:
            left_hand_row = list(np.array([['N/A', 'N/A'] for i in range(21)]).flatten())
        
        try:
            right_hand = results.right_hand_landmarks.landmark
            right_hand_row = list(np.array([[landmark.x * image_height, landmark.y * image_height] for landmark in right_hand]).flatten())
        except:
            right_hand_row = list(np.array([['N/A', 'N/A'] for i in range(21)]).flatten())

        row = face_row + pose_row + left_hand_row + right_hand_row + category
                                                                    ##
        framelist.append(row)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    

    cap.release()
    cv2.destroyAllWindows()

landmarks = []

for val in range(1, 544):
#     landmarks += ['x{}'.format(val), 'y{}'.format(val), 'z{}'.format(val), 'v{}'.format(val)]
    landmarks += ['x{}'.format(val), 'y{}'.format(val)]

landmarks.append('class')

df = pd.DataFrame(framelist, columns= landmarks)
print(df.shape)
df.to_csv(os.getcwd() + "/Users/LJH/특징점.csv", index= True, encoding= 'euc-kr')

numpyData = df.to_numpy

print(numpyData)