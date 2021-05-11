import cv2
import mediapipe as mp
import os
import pandas as pd
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

#For static images:
file_list = os.listdir("/Users/tuan/Documents/University/3학년/설계및프로젝트/Project_KSLDeepLearning/face_test/data")

data = []
df = pd.DataFrame(data)

face_List = []
left_hand_List = []
right_hand_List = []
pose_List = []

with mp_holistic.Holistic(
    static_image_mode=True,
    model_complexity=2) as holistic:
  for idx, file in enumerate(file_list):
    if file == ".DS_Store":
            continue

    imagePath = os.path.abspath(file)
    image = cv2.imread("/Users/tuan/Documents/University/3학년/설계및프로젝트/Project_KSLDeepLearning/face_test/data/test.jpg")
    image_height, image_width, _ = image.shape
    # Convert the BGR image to RGB before processing.
    global results 
    results = holistic.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    if results.pose_landmarks:
      print(
          f'Nose coordinates: ('
          f'{results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].x * image_width}, '
          f'{results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].y * image_height})'
      )
    # Draw pose, left and right hands, and face landmarks on the image.
    annotated_image = image.copy()
    mp_drawing.draw_landmarks(
        annotated_image, results.face_landmarks, mp_holistic.FACE_CONNECTIONS)
    myFace = results.face_landmarks
    id_count = 0
    for id, lm in enumerate(myFace.landmark):
        h, w, c = annotated_image.shape
        cx, cy = int(lm.x * w), int(lm.y * h)
        face_List.extend([cx, cy])
        id_count += 1

    face_col_list = []

    for i in range(id_count):
        suffix = ['_x', '_y']
        for j in suffix:
            face_col_list.append("face_" + str(i) + j)

    df_face = pd.DataFrame(columns= face_col_list)
    df_face.loc[idx] = face_List
    id_count = 0
    
    mp_drawing.draw_landmarks(
        annotated_image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
    myLeftHand = results.left_hand_landmarks
    for id, lm in enumerate(myLeftHand.landmark):
        h, w, c = annotated_image.shape
        cx, cy = int(lm.x * w), int(lm.y * h)
        left_hand_List.extend([cx, cy])
        id_count += 1

    left_hand_col_list = []

    for i in range(id_count):
        suffix = ['_x', '_y']
        for j in suffix:
            left_hand_col_list.append("left_hand_" + str(i) + j)

    df_left_hand = pd.DataFrame(columns= left_hand_col_list)
    df_left_hand.loc[idx] = left_hand_List
    id_count = 0

    mp_drawing.draw_landmarks(
        annotated_image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
    myRightHand = results.right_hand_landmarks
    for id, lm in enumerate(myRightHand.landmark):
        h, w, c = annotated_image.shape
        cx, cy = int(lm.x * w), int(lm.y * h)
        right_hand_List.extend([cx, cy])
        id_count += 1

    right_hand_col_list = []

    for i in range(id_count):
        suffix = ['_x', '_y']
        for j in suffix:
            right_hand_col_list.append("right_hand_" + str(i) + j)

    df_right_hand = pd.DataFrame(columns= right_hand_col_list)
    df_right_hand.loc[idx] = right_hand_List
    id_count = 0

    mp_drawing.draw_landmarks(
        annotated_image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
    myPose = results.pose_landmarks
    for id, lm in enumerate(myPose.landmark):
        h, w, c = annotated_image.shape
        cx, cy = int(lm.x * w), int(lm.y * h)
        pose_List.extend([cx, cy])
        id_count += 1

    pose_col_list = []

    for i in range(id_count):
        suffix = ['_x', '_y']
        for j in suffix:
            pose_col_list.append("pose_" + str(i) + j)

    df_pose = pd.DataFrame(columns= pose_col_list)
    df_pose.loc[idx] = pose_List
    id_count = 0

    df_total = pd.concat([df_face, df_left_hand, df_right_hand, df_pose], axis=1)
    print(df_total)


df_total.to_csv('/Users/tuan/Documents/University/3학년/설계및프로젝트/Project_KSLDeepLearning/face_test/특징점.csv')

