import cv2
from os import listdir , makedirs
from os.path import isfile, join, exists

import sys

import msvcrt

import shutil
import threading
import time

# source = "D:\\folder\\New folder (3)\\0000new photos random/"
source = "assets/"
dest = "sorted/"

list = [f for f in listdir(source) if isfile(join(source, f))]

keep_going = True
mutex = threading.Lock()


H = 1440
W = 2560


def showImg(file):
    split = file.split('.')
    extension = split[len(split) - 1]

    if extension in ["jpg", "png" , "jpeg", "webp"]:
        global thPic
        thPic = threading.Thread(target=showPic, args=(file,), name="Show pic Thread: " + file)
        thPic.start()
        return thPic

    elif extension == "gif":
        # capture the animated gif
        p = "{p}{l}".format(p=source, l=file)
        global thGif
        thGif = threading.Thread(target=showGifThread, args=(p,), name="Show Gif Thread: " + file, daemon=None)
        thGif.start()
        return thGif


def showPic(file):

    print("showing " + file + " thread \n")

    imagePath = "{p}{l}".format(p=source, l=file)

    img = cv2.imread(imagePath)

    height = img.shape[0]
    width = img.shape[1]

    window_name = "original " + file

    while keep_going:
        if height > 1440 or width > 2560:
            # define the screen resulation
            window_name = 'Resized Window ' + file
            screen_res = W, H
            scale_width = screen_res[0] / img.shape[1]
            scale_height = screen_res[1] / img.shape[0]
            scale = min(scale_width, scale_height)
            # resized window width and height
            window_width = int(img.shape[1] * scale)
            window_height = int(img.shape[0] * scale)
            # cv2.WINDOW_NORMAL makes the output window resizealbe
            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
            # resize the window according to the screen resolution
            cv2.resizeWindow(window_name, window_width, window_height)
            cv2.setWindowProperty(window_name , cv2.WND_PROP_FULLSCREEN, cv2.WND_PROP_FULLSCREEN)
            cv2.imshow(window_name, img)
            cv2.waitKey(1)
        else:
            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
            cv2.setWindowProperty(window_name , cv2.WND_PROP_FULLSCREEN, cv2.WND_PROP_FULLSCREEN)
            cv2.imshow(window_name, img)
            cv2.waitKey(1)

    cv2.destroyAllWindows()



def showGifThread(file):
    print("showing " + file + " thread \n")

    gif = cv2.VideoCapture(file)
    frames = []
    ret = True  # ret=True if it finds a frame else False.
    while ret:
        # read next frame
        ret, frame = gif.read()
        if not ret:
            break
        frames.append(frame)
    c = 0

    height = frames[0].shape[0]
    width = frames[0].shape[1]

    window_name = "original " + file

    global keep_going
    while keep_going:
        if c < len(frames):

            # cv2.imshow(path, frames[c])
            # cv2.waitKey(100)
            img = frames[c]
            if height > 1440 or width > 2560:
                window_name = 'Resized Window ' + source
                # define the screen resulation
                screen_res = W, H
                scale_width = screen_res[0] / img.shape[1]
                scale_height = screen_res[1] / img.shape[0]
                scale = min(scale_width, scale_height)
                # resized window width and height
                window_width = int(img.shape[1] * scale)
                window_height = int(img.shape[0] * scale)
                # cv2.WINDOW_NORMAL makes the output window resizealbe
                cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
                # resize the window according to the screen resolution
                cv2.resizeWindow(window_name, window_width, window_height)
                cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WND_PROP_FULLSCREEN)
                cv2.imshow(window_name, img)
                cv2.waitKey(50)
            else:
                cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
                cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WND_PROP_FULLSCREEN)
                cv2.imshow(window_name, img)
                cv2.waitKey(50)
            c += 1

        else:
            c = 0
    cv2.destroyAllWindows()


def start():

    if not exists('{dest}/bu'.format(dest=dest)):
        makedirs('{dest}/bu'.format(dest=dest))

    if not exists('{dest}/fe'.format(dest=dest)):
        makedirs('{dest}/fe'.format(dest=dest))

    if not exists('{dest}/bo'.format(dest=dest)):
        makedirs('{dest}/bo'.format(dest=dest))

    if not exists('{dest}/fff'.format(dest=dest)):
        makedirs('{dest}/fff'.format(dest=dest))

    if not exists('{dest}/irl'.format(dest=dest)):
        makedirs('{dest}/irl'.format(dest=dest))

    if not exists('{dest}/skipped'.format(dest=dest)):
        makedirs('{dest}/skipped'.format(dest=dest))


    for x in list:
        th = showImg(x)
        takeinput(x)
        global keep_going
        keep_going = False
        th.join()

def test():
    inputs = [2, 0, 1, 0]
    i = 0
    while (i < len(inputs)):
        global keep_going
        showImg(inputs[i])
        i += 1
        time.sleep(4)
        keep_going = False
        time.sleep(1)


def takeinput(x):
    global keep_going
    keep_going = True
    c = input("1 for bu, 2 for fe, 3 for bobs, 4 for fff , 5 for irl or anything else to skip  and X to exit \n")

    # print("1 for bu, 2 for fe, 3 for bobs, 4 for fff , 5 for irl or anything else to skip  and X to exit \n")
    # c = msvcrt.getch()

    print(c)


    time.sleep(0.1)

    if c == "1":
        shutil.move("{path}{x}".format(path=source, x=x), "{dest}/bu/{x}".format(dest=dest, x=x))
    elif c == "2":
        shutil.move("{path}{x}".format(path=source, x=x), "{dest}/fe/{x}".format(dest=dest, x=x))
    elif c == "3":
        shutil.move("{path}{x}".format(path=source, x=x), "{dest}/bo/{x}".format(dest=dest, x=x))
    elif c == "4":
        shutil.move("{path}{x}".format(path=source, x=x), "{dest}/fff/{x}".format(dest=dest, x=x))
    elif c == "5":
        shutil.move("{path}{x}".format(path=source, x=x), "{dest}/irl/{x}".format(dest=dest, x=x))
    elif c == "x":
        keep_going = False
        quit(0)
    else:
        shutil.move("{path}{x}".format(path=source, x=x), "{dest}/skipped/{x}".format(dest=dest, x=x))


print(list)
start()

cv2.destroyAllWindows()  # destroys the window showing image
