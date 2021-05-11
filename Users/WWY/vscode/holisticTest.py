import cv2
import mediapipe as mp
import fileControlModule as fcm
import pandas as pd
import os
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

# 경로 설정
Path = "./newimage"
fc = fcm.fileControl(Path)
file_list = fc.makeFileList(0)

# 데이터프레임 생성
posedf = pd.DataFrame()
posedf.columns('as', 'ab')


# For static images:
with mp_holistic.Holistic(static_image_mode=True) as holistic:
    for idx, file in enumerate(file_list):
        filepath = fc.getfilepath(file)
        image = cv2.imread(filepath)
        image_height, image_width, _ = image.shape
        # Convert the BGR image to RGB before processing.
        results = holistic.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        poseList = []
        # if results.pose_landmarks:
        #     myPose = results.pose_landmarks
        #     for id, lm in enumerate(myPose.landmark):
        #         poseList.append([id, lm.x, lm.y])
        myPose = results.pose_landmarks
        for id, lm in enumerate(myPose.landmark):
            poseList.append([id, lm.x, lm.y])
        # print(
        #     f'Nose coordinates: ('
        #     f'{results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].x * image_width}, '
        #     f'{results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].y * image_height})'
        # )
        # Draw pose, left and right hands, and face landmarks on the image.
        annotated_image = image.copy()
        mp_drawing.draw_landmarks(
            annotated_image, results.face_landmarks, mp_holistic.FACE_CONNECTIONS)
        mp_drawing.draw_landmarks(
            annotated_image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        mp_drawing.draw_landmarks(
            annotated_image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        # Use mp_holistic.UPPER_BODY_POSE_CONNECTIONS for drawing below when
        # upper_body_only is set to True.
        mp_drawing.draw_landmarks(
            annotated_image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
        print(poseList)
        
        # 파일 저장하기
        # cv2.imwrite('./holistic/annotated_image' +
        #             str(idx) + '.png', annotated_image)

# For webcam input:
# cap = cv2.VideoCapture(0)
# with mp_holistic.Holistic(
#     min_detection_confidence=0.5,
#     min_tracking_confidence=0.5) as holistic:
#   while cap.isOpened():
#     success, image = cap.read()
#     if not success:
#       print("Ignoring empty camera frame.")
#       # If loading a video, use 'break' instead of 'continue'.
#       continue

#     # Flip the image horizontally for a later selfie-view display, and convert
#     # the BGR image to RGB.
#     image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
#     # To improve performance, optionally mark the image as not writeable to
#     # pass by reference.
#     image.flags.writeable = False
#     results = holistic.process(image)

#     # Draw landmark annotation on the image.
#     image.flags.writeable = True
#     image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
#     mp_drawing.draw_landmarks(
#         image, results.face_landmarks, mp_holistic.FACE_CONNECTIONS)
#     mp_drawing.draw_landmarks(
#         image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
#     mp_drawing.draw_landmarks(
#         image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
#     mp_drawing.draw_landmarks(
#         image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
#     cv2.imshow('MediaPipe Holistic', image)
#     if cv2.waitKey(5) & 0xFF == 27:
#       break
# cap.release()
