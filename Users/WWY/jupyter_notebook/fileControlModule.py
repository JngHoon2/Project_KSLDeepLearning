import os
import cv2


class fileControl():
    def __init__(self, Path):
        self.rootPath = Path  # 데이터 각 폴더들의 상위 폴더 1개에 대한 경로
        self.folders = os.listdir(self.rootPath)  # 이미지 더미가 들어있는 각각의 폴더들 저장
        # 임시적으로 첫번째 폴더에 대한 경로
        # self.folderPath = f'{self.rootPath}/{self.folders[0]}' #makeFileList에 idx주는걸로 옮겨짐

    def makeFileList(self, idx):
        self.folderPath = f'{self.rootPath}/{self.folders[idx]}'
        self.file_list = os.listdir(self.folderPath)

        return self.file_list

    def getfilepath(self, filename):
        self.path = f'{self.folderPath}/{filename}'
        return self.path


def main():
    Path = "./sample"
    fc = fileControl('./sample')
    file_list = fc.makeFileList(0)
    # print(fc.makeFileList(0))
    filepath = fc.getfilepath('01_77.0001.jpg')
    # print(filepath)
    print(filepath)
    image = cv2.imread(filepath)
    # print(image)


if __name__ == "__main__":
    main()

# 이미지 폴더 접근 코드

# overlayList = []
# for imPath in myList:
#     image = cv2.imread(f'{folderPath}/{imPath}')
#     # print(f'{folderPath}/{imPath}')
#     overlayList.append(image) #위에 얹어질 손모양 이미지의 파일명을 리스트로 추가
