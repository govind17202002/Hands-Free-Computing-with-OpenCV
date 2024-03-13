import cv2 as cv
import mediapipe as mp

class handDetector():



    #   Initialising default:
    def __init__(self, mode=False, max_num_hands=2,
                 model_complexity=1, detectCon=0.5, trackCon=0.5):

               self.mode = mode
               self.max_num_hands = max_num_hands
               self.detectCon = detectCon
               self.trackCon = trackCon
               self.mpHands = mp.solutions.hands
               self.hands = self.mpHands.Hands(self.mode, self.max_num_hands,
                            model_complexity, self.detectCon, self.trackCon)
               self.mpDraw = mp.solutions.drawing_utils



    def findHands(self, image, draw=True):

        imgRGB = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        self.output = self.hands.process(imgRGB)

        if self.output.multi_hand_landmarks:  # are there multiple-hand?
            for handLms in self.output.multi_hand_landmarks:  # Hand-Landmarks
                if draw:
                    # Draw Hand-Landmarks
                    self.mpDraw.draw_landmarks(image, handLms, self.mpHands.HAND_CONNECTIONS,
                    self.mpDraw.DrawingSpec(color=(248, 226, 225), thickness=2, circle_radius=1),
                    self.mpDraw.DrawingSpec(color=(60, 40, 83), thickness=3, circle_radius=2))
                    # NOTE:   Last two parameters: hand points, line-connection
        return image



    def findPosition(self, image, handNo=0, draw=True):
        # Return landmarks of primary-hand

        lmList = []
        if self.output.multi_hand_landmarks:
            myHand = self.output.multi_hand_landmarks[handNo]
            for id, landmark in enumerate(myHand.landmark):  # position of each landmark [id: 0 <--->20]
                # frame/screen size
                image_h, image_w, _ = image.shape
                # get co-ordinates/pixels of each landmark:
                x, y = int(landmark.x * image_w), int(landmark.y * image_h)
                lmList.append([id, x, y])
                if draw:
                    cv.circle(image, (x, y), 5, (58, 62, 58))
        return lmList



    def statusFingers(self, lmList):

        f_status = []
        # Thumb-Id
        f_status.append((lmList[3][1]-lmList[4][1]) > 15)
        # Other Fingers-id
        f_id = [8, 12, 16, 20]
        for id in f_id:
            f_status.append(lmList[id][2] < lmList[id-2][2])

        return f_status



    def configElements(self, image, lmList, draw=True):

        #   define elements
        thumb = lmList[4][1], lmList[4][2]
        index = lmList[8][1], lmList[8][2]
        middle = lmList[12][1], lmList[12][2]

        #   Colouring elements
        if draw:
            cv.circle(image, index, 7, (76, 65, 64), 4)
            # cv.circle(image, thumb, 7, (76, 65, 64), 3)
            # cv.circle(image, middle, 7, (255, 255, 0), 2)

        return index




def main():

    capture = cv.VideoCapture(0)
    capture.set(3, 640)
    capture.set(4, 480)
    detector = handDetector()
    while True:
        success, image = capture.read()
        image = cv.flip(image, 1)
        image = detector.findHands(image)
        # land-mark coordinates according to image resolution
        lmList = detector.findPosition(image)
        # # lmList ->  [id, x, y]
        if len(lmList) != 0:

            f_status = detector.statusFingers(lmList)
            # Cursor_pos (index-finger)
            # According to Screen-size
            x, y = detector.configElements(image, lmList)
            print(f_status)


        cv.imshow('WebCam', image)
        cv.waitKey(1)

if __name__ == "__main__":
    main()