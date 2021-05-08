import cv2
import mediapipe as mp
import os
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

# For static images:
file_list = os.listdir("/Users/tuan/Documents/University/3학년/설계및프로젝트/Project_KSLDeepLearning/face_test/data")
f = open("/Users/tuan/Documents/University/3학년/설계및프로젝트/Project_KSLDeepLearning/face_test/특징점.txt", 'w')

with mp_holistic.Holistic(
    static_image_mode=True,
    model_complexity=2) as holistic:
  for idx, file in enumerate(file_list):
    
    imagePath = os.path.abspath(file)
    image = cv2.imread("/Users/tuan/Documents/University/3학년/설계및프로젝트/Project_KSLDeepLearning/face_test/data/test.jpg")
    image_height, image_width, _ = image.shape
    # Convert the BGR image to RGB before processing.
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
    f.write("face_landmarks \n" + str(mp_holistic.FACE_CONNECTIONS) + "\n ==================================== \n")
    print("face_landmarks \n" + str(mp_holistic.FACE_CONNECTIONS) + "\n ==================================== \n")

    mp_drawing.draw_landmarks(
        annotated_image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
    f.write("left_hand_landmarks \n" + str(mp_holistic.HAND_CONNECTIONS) + "\n ==================================== \n")
    print("left_hand_landmarks \n" + str(mp_holistic.HAND_CONNECTIONS) + "\n ==================================== \n")

    mp_drawing.draw_landmarks(
        annotated_image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
    f.write("right_hand_landmarks \n" + str(mp_holistic.HAND_CONNECTIONS) + "\n ==================================== \n")
    print("right_hand_landmarks \n" + str(mp_holistic.HAND_CONNECTIONS) + "\n ==================================== \n")

    mp_drawing.draw_landmarks(
        annotated_image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
    f.write("pose_landmarks \n" + str(mp_holistic.POSE_CONNECTIONS) + "\n ==================================== \n")
    print("pose_landmarks \n" + str(mp_holistic.POSE_CONNECTIONS) + "\n ==================================== \n")

    cv2.imwrite("/Users/tuan/Documents/University/3학년/설계및프로젝트/Project_KSLDeepLearning/face_test/" + str(idx) + '.jpg', annotated_image)

f.close()

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
#        image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
#     mp_drawing.draw_landmarks(
#         image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
#     cv2.imshow('MediaPipe Holistic', image)
#     if cv2.waitKey(5) & 0xFF == 27:
#       break
# cap.release()