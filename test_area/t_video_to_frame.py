import cv2
import os
import pickle
from os.path import join, exists
import t_handsegment as hs
import argparse
from tqdm import tqdm

hc = [] # hc 라는 이름의 리스트를 정의합니다.


def convert(gesture_folder, target_folder):
    rootPath = os.getcwd()                      # rootPath 변수에 현재 디렉토리의 위치를 저장합니다.
    majorData = os.path.abspath(target_folder)  # majorData 변수에 target_foler의 정규화된 절대 경로명을 저장합니다. 

    if not exists(majorData):                   # majorData 변수에 저장된 폴더가 존재하는 지 확인합니다. exists(x)-> x가 존재하면 True 반환 
        os.makedirs(majorData)                  # majorData 라는 이름의 폴더를 생성합니다.

    gesture_folder = os.path.abspath(gesture_folder) # gesture_folder 변수에 함수에서 받은 매개 변수 gesture_folder의 정규절대경로명을 저장합니다.

    os.chdir(gesture_folder)                            # 현재 디렉토리의 경로를 gesture_folder 로 변경합니다.
    gestures = os.listdir(os.getcwd())                  # gestures 라는 변수에 현재 디렉토리의 리스트를 저장합니다.

    print("Source Directory containing gestures: %s" % (gesture_folder))
    print("Destination Directory containing frames: %s\n" % (majorData))

    # gestures 리스트의 인덱스를 통해 반복문을 실행합니다. unit은 단위명을 지정하며  ascii가 True인 것은 진행바가 #로 표현됩니다.
    for gesture in tqdm(gestures, unit='actions', ascii=True): 
        if gesture == ".DS_Store":
            continue

        gesture_path = os.path.join(gesture_folder, gesture) # gesture_path 변수에 gesture_folder와 gesture 의 경로명을 합친 값을 저장합니다.
        os.chdir(gesture_path)                               # 현재 디렉토리의 경로를 gesture_path 로 변경합니다.

        gesture_frames_path = os.path.join(majorData, gesture) # gesture_frames_path 변수에 majorData와 gesture의 경로명을 합친 값을 저장합니다.
        if not os.path.exists(gesture_frames_path):            # gesture_frames_path 폴더가 존재하는 지 확인합니다. 
            os.makedirs(gesture_frames_path)                   # gesture_frames_path 라는 이름의 폴더를 생성합니다.

        videos = os.listdir(os.getcwd())                                # videos 라는 변수에 현재 디렉토리의 리스트를 저장합니다.
        videos = [video for video in videos if(os.path.isfile(video))]  # videos 리스트의 인덱스(video)가 존재하면 video를 반환하여 videos리스트에 저장합니다

        # videos 리스트의 인덱스를 통해 반복문을 실행합니다. unit은 단위명을 지정하며  ascii가 True인 것은 진행바가 #로 표현됩니다.
        for video in tqdm(videos, unit='videos', ascii=True):
            if video == ".DS_Store":
                continue

            name = os.path.abspath(video)                       # 인덱스의 경로명을 name 변수에 저장합니다.
            cap = cv2.VideoCapture(name)                        # capturing input video / name 비디오를 이용합니다.
            frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) # 사용한 비디오의 프레임 수를 저장합니다.
            lastFrame = None                                    # lastFrame 변수를 NULL 상태로 정의합니다.

            os.chdir(gesture_frames_path)                       # 현재 경로를 gesture_frames_path 로 변경합니다.
            count = 0                                           # count 변수가 0인 상태로 정의됩니다.

            # assumption only first 200 frames are important / 비디오에서 처음 200 프레임만 따옵니다.
            while count < 200:
                ret, frame = cap.read()  # extract frame / 파일을 읽습니다. 성공시 수신한 바이트 수를 리턴하며 실패시 -1을 반환합니다.
                if ret is False:         # 파일을 읽는 것을 실패하면 반복문을 종료합니다.
                    if count > 1 :
                        print(" \n Total Frame_Count :" + str(count))
                        break
                    print(" \n WARNING!! VIDEO_READ_FAIL")
                    break
                framename = os.path.splitext(video)[0]                                  # 파일의 확장자를 따옵니다.
                framename = framename + "_frame_" + str(count) + ".jpeg"                # 프레임 이미지의 이름을 재정의 합니다.
                hc.append([join(gesture_frames_path, framename), gesture, frameCount])  # hc리스트에 이미지의 경로와 제스쳐, 프레임 수를 추가합니다.

                if not os.path.exists(framename):                   # 이미지의 존재 여부를 확인합니다.
                    frame = hs.handsegment(frame)                   # handsegement의 리턴값을 frame에 저장합니다.
                    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # 이미지의 색상을 BGR기준으로 GRAY로 변경합니다.
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
                    lastFrame = frame                              
                    cv2.imwrite(framename, frame)                   # 파일을 저장합니다.

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                count += 1

            # repeat last frame untill we get 200 frames
            while count < 201:
                framename = os.path.splitext(video)[0]
                framename = framename + "_frame_" + str(count) + ".jpeg"
                hc.append([join(gesture_frames_path, framename), gesture, frameCount])
                if not os.path.exists(framename):
                    cv2.imwrite(framename, lastFrame)
                count += 1

            os.chdir(gesture_path)  # 현재 디렉토리의 경로를 gesture_path 로 변경합니다.
            cap.release()           # 오픈한 캡쳐 객체를 해제합니다.
            cv2.destroyAllWindows() # 열린 모든 창을 닫습니다.

    os.chdir(rootPath) # 현재 디렉토리의 위치를 rootPath로 변경합니다.

if __name__ == '__main__':
    gesture_folder = "/Users/tuan/Documents/University/3학년/설계및프로젝트/Project_KSLDeepLearning/test_area/data"
    target_folder = "/Users/tuan/Documents/University/3학년/설계및프로젝트/Project_KSLDeepLearning/test_area/image_JKH"
    convert(gesture_folder, target_folder)