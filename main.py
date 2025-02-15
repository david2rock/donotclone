import numpy as np
import cv2
from cvzone.HandTrackingModule import HandDetector  # type: ignore

from cvzone.FPS import FPS  # type: ignore
import pyautogui  # type: ignore
import utils

# Configuration
wCam, hCam = 640, 480
wScr, hScr = pyautogui.size()
frameR = 110
swipeCounter = 0
swipeMode = None
gestureDelay = 15
slected_tool = None
smooth = 5
plocx, plocy = 0, 0
clocx, clocy = 0, 0

# Camera and HandDetector Setup
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


dr = HandDetector(maxHands=1)
fps_counter = FPS()

# Main loop
while cap.isOpened():
    _, img = cap.read()
    img = cv2.resize(img, (640, 480))

    fps_counter.update(img, scale=2, thickness=3)

    hands, img = dr.findHands(img, flipType=False)
    if hands:
        hand = hands[0]
        lmList = hand["lmList"]
        fingers = dr.fingersUp(hand)
        thump_tip = lmList[4][0:2]
        index_knucle = lmList[6][0:2]

        length, info, _ = dr.findDistance(thump_tip, index_knucle)
        fingers[0] = 0 if length <= 27 else 1

        index_tip = lmList[8][:2]

        px = np.interp(index_tip[0], (frameR, wCam - frameR), (0, wScr))
        py = np.interp(index_tip[1], (frameR, hCam - frameR), (0, hScr))

        # Smooth mouse movement
        clocx = plocx + (px - plocx) / smooth  # type: ignore
        clocy = plocy + (py - plocy) / smooth  # type: ignore

        cv2.rectangle(
            img, (frameR, frameR), (wCam - frameR, hCam - frameR), (0, 0, 0), 2
        )

        # Gesture Detection
        if fingers[0] == 1 and fingers[4] == 1:
            swipeMode = None

        elif fingers == [1, 0, 0, 0, 0]:
            img = utils.displayText("Thumb up: Move right", img)
            swipeMode = "right"

        elif fingers == [0, 0, 0, 0, 1]:
            img = utils.displayText("Pinky up: Move left", img)
            swipeMode = "left"

        # Tool mode detection
        elif fingers == [0, 1, 0, 0, 0]:
            img = utils.displayText("Index up: Laser mode", img)

            cv2.circle(img, index_tip, 7, (255, 0, 0), cv2.FILLED)
            if slected_tool != "laser":
                slected_tool = utils.toggleAction("laser")
            utils.mouseAction(int(clocx), int(clocy), "move")

        elif fingers == [0, 1, 1, 0, 0]:
            img = utils.displayText("Index & middle up: Highlighter mode", img)

            cv2.circle(img, index_tip, 7, (255, 0, 0), cv2.FILLED)
            if slected_tool != "highlighter":
                slected_tool = utils.toggleAction("highlighter")
            utils.mouseAction(int(clocx), int(clocy), "drag")

        elif fingers == [0, 1, 1, 1, 0]:
            img = utils.displayText("Index, middle & ring up: eraser mode", img)

            cv2.circle(img, index_tip, 7, (255, 0, 0), cv2.FILLED)
            if slected_tool != "eraser":
                slected_tool = utils.toggleAction("eraser")
            utils.mouseAction(int(clocx), int(clocy), "drag")

        plocx, plocy = clocx, clocy

        # Swipe gesture execution
        if swipeMode:
            swipeCounter += 1
            if swipeCounter >= gestureDelay:
                utils.swipe(swipeMode)
                swipeMode = None
                swipeCounter = 0

    cv2.imshow("Hand Tracking", img)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
