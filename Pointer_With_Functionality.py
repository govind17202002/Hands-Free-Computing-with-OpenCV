import cv2 as cv
import numpy as np
import time
import pyautogui as pgi
import autopy
import Cursor_Pointer



def main():

    capture = cv.VideoCapture(0)
    capture.set(3, 640)
    capture.set(4, 480)
    detector = Cursor_Pointer.handDetector(trackCon=0.7)

#   Smooth-Scrolling
    smooth = 6
    prev_X, prev_Y = 0, 0
    curr_X, curr_Y = 0, 0
    frameR = 130    # Frame Reduction


    while True:
        success, image = capture.read()
        image = cv.flip(image, 1)
        image = detector.findHands(image)
        lmList = detector.findPosition(image)
        height, width, _ = image.shape
        screen_width, screen_height = autopy.screen.size()

        if len(lmList) != 0:        # If hand present :

            f_status = detector.statusFingers(lmList)
            print(f_status)
            # To configure Hands
            detector.configElements(image, lmList)

            x, y = lmList[8][1:]

            if f_status[2] and f_status[3] and f_status[4] and (not f_status[1]):
                pgi.scroll(500)
                time.sleep(0.45)
            elif f_status[1] and f_status[2] and f_status[3]:
                pgi.scroll(-500)
                time.sleep(0.45)
            elif f_status[1] and f_status[2] and not (f_status[0] or f_status[4]):
                pgi.rightClick()
                time.sleep(0.2)
            elif f_status[1] and f_status[4] and (not f_status[0]):
                pgi.mouseDown()
                time.sleep(0.25)
            elif f_status[1] and f_status[0]:
                pgi.click()
                time.sleep(0.25)
            elif f_status[1]:
                X = np.interp(x, (frameR, width - frameR), (0, screen_width))
                Y = np.interp(y, (frameR, height - frameR), (0, screen_height))
                # Cursor Position (X, Y)
                curr_X = prev_X + (X - prev_X)/smooth
                curr_Y = prev_Y + (Y - prev_Y)/smooth
                autopy.mouse.move(curr_X, curr_Y)
                prev_X, prev_Y = curr_X, curr_Y
            elif f_status[0] and f_status[4]:
                with pgi.hold('win'):
                    pgi.press('h')
                time.sleep(0.25)
            elif f_status[0]:
                pgi.press('volumedown')
                time.sleep(0.15)
            elif f_status[4]:
                pgi.press('volumeup')
                time.sleep(0.15)




        cv.imshow('WebCam', image)
        cv.waitKey(1)

if __name__ == "__main__":
    main()