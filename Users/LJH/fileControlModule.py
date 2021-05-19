import os
from os import path
import cv2


class fileControl():

    # def chooseGesture(self):
    #     return 


    def chooseGesture(self, folder, index):
        folderlist = os.listdir(folder)
        if ".DS_Store" in folderlist:
            folderlist.remove(".DS_Store")

        return os.path.join(folder, folderlist[index])


    def chooseFile(self, folder, index):
        filelist = os.listdir(folder)
        if ".DS_Store" in filelist:
            filelist.remove(".DS_Store")

        return os.path.join(folder, filelist[index])



# main 함수는 테스트용

def main():
    Path = os.getcwd()
    fc = f'{Path}/{"Users/LJH/data"}'
    print(fc)

    fcc = fileControl()

    gtest = fcc.chooseGesture(fc, 0)
    print(gtest)
    ftest = fcc.chooseFile(gtest, 0)
    print(ftest)


if __name__ == "__main__":
    main()