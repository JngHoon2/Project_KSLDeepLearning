import cv2
import time
import os
import HandTrackingModule as htm
import fileControlModule as fcm

# 캠 창 크기 설정
wCam, hCam = 640, 480
# 캠코더 설정 0 : 내장 , 1 : 외장
cap = cv2.VideoCapture(0)
# https://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html#videocapture-get
# 3번과 4번은 각각 캠의 너비와 높이를 지정하는 속성 property
cap.set(3, wCam)
cap.set(4, hCam)

# 이미지 폴더 접근 코드
# folderPath = "FingerImages"
# myList = os.listdir(folderPath)
# print(myList)
# overlayList = []
# for imPath in myList:
#     image = cv2.imread(f'{folderPath}/{imPath}')
#     # print(f'{folderPath}/{imPath}')
#     overlayList.append(image) #위에 얹어질 손모양 이미지의 파일명을 리스트로 추가

# print(len(overlayList))
pTime = 1

detector = htm.handDetector(detectionCon=0.75)

#엄지, 검지, 중지, 약지, 소지
tipIds = [4, 8, 12, 16, 20]

# 카메라 동작하는 부분 코드
while True:
    success, img = cap.read()
    img = detector.findHands(img)

    # 좌표를 추적, draw = true시에 분홍점을 찍음
    lmList = detector.findPosition(img, draw=True)
    # print(lmList)

    if len(lmList) != 0:  # 손이 감지가 된 상태에서
        fingers = []
        # 랜드마크는 각 지점별로 좌표가 있고, 3개의 위치, x값, y값의 2차원 배열로 리스트에 저장되어있다.
        # 따라서 8번인 검지끝의 y값이 검지 중간마디 y값보다 작으면 손가락이 펴져있다는 뜻, 아닌 경우 웅크렸다는 뜻
        # 이 프로젝트의 목표는 딥러닝 모델이 이러한 경향을 스스로 학습하여 어떤 손모양을 하고있고
        # 그 손모양이 어떤 수어의 의미를 담고 있는지 분류할 수 있는 것을 만드는 것이다.

        # if lmList[8][2] < lmList[6][2]: # [랜드마크 좌표값][랜드마크 좌표, x, y]
        #     print("손바닥 펴짐, 보자기")
        # else:
        #     print("손 웅크림, 주먹")

        # 엄지손가락은 x축을 기준으로 접었는지 폈는지 확인, 캠이 좌우반전 되어있으므로 왼손 기준으로
        # x 값이 엄지 끝 < 엄지 안쪽 마디 인경우 끝이 더 왼쪽에 있는것이므로 펴져있는걸로 인식
        if lmList[tipIds[0]][1] < lmList[tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 나머지손가락은 y축에 영향
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        # print(fingers)
        totalFingers = fingers.count(1)  # 1인경우의 개수를 센다
        # print(totalFingers)

        # 손가락 이미지에 대해서 표시하는 코드
        #h, w, c = overlayList[totalFingers -1].shape
        #img[0:h, 0:w] = overlayList[totalFingers-1]

        cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (45, 375),
                    cv2.FONT_HERSHEY_PLAIN, 10, (2))

    # 오버레이 이미지 출력설정
    # h, w, c = overlayList[0].shape
    # img[0:h, 0:w] = overlayList[0]

    # fps 표시
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 0, 0), 3)

    # 이미지 띄우기 및 종료문
    cv2.imshow("image", img)
    if cv2.waitKey(1) > 0:
        break

# file_list = fcm.fileControl("sample").makeFileList()

# for idx, file in enumerate(file_list):
#     image = cv2.flip(cv2.imread(file), 1)

#     result = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

#     print('Handedness:', results.multi_handedness)

#     # 손 디텍션 못하면 예외처리
#     if not results.multi_hand_landmarks:
#         continue

#     image_height, image_width, _ = image.shape
#     annotated_image = image.copy()
#     for hand_landmarks in results.multi_hand_landmarks:
#         print('hand_landmarks:', hand_landmarks)
#         print(
#             f'Index finger tip coordinates: (',
#             f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
#             f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
#         )
#         mp_drawing.draw_landmarks(
#             annotated_image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
#     cv2.imwrite(
#         '/tmp/annotated_image'+str(idx) + '.png', cv2.flip(annotated_image, 1)
#     )
