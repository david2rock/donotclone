import cv2
import numpy as np
import pyautogui  # type: ignore
from cvzone.FPS import FPS  # type: ignore
from cvzone.HandTrackingModule import HandDetector  # type: ignore

import utils

# Configuration
wCam, hCam = 640, 480
wScr, hScr = pyautogui.size()
frameR = 110
swipeCounter = 0
swipeMode = None
gestureDelay = 15
selected_tool = None
smooth = 5
plocx, plocy = 0, 0
clocx, clocy = 0, 0

# Camera and HandDetector Setup
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, wCam)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, hCam)

if not cap.isOpened():
    print("Error: Could not open the camera.")
    exit()

dr = HandDetector(maxHands=1)
fps_counter = FPS()

try:
    # Main loop
    while cap.isOpened():
        _, img = cap.read()
        img = cv2.flip(img, 1)
        if img is None:
            print("Error: Failed to capture frame.")
            break

        img = cv2.resize(img, (wCam, hCam))
        fps_counter.update(img, scale=2, thickness=3)

        hands, img = dr.findHands(img)
        if hands:
            hand = hands[0]
            lmList = hand["lmList"]
            fingers = dr.fingersUp(hand)
            thumb_tip = lmList[4][0:2]
            index_knuckle = lmList[6][0:2]

            index_tip = lmList[8][:2]

            # Map index finger position to screen coordinates
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
                if selected_tool != "laser":
                    selected_tool = utils.toggleAction("laser")
                pyautogui.moveTo(clocx, clocy, duration=0.1)

            elif fingers == [0, 1, 1, 0, 0]:
                img = utils.displayText("Index & middle up: Highlighter mode", img)
                length, _, img = dr.findDistance(index_tip, lmList[12][:2], img)
                if length <= 35:
                    if selected_tool != "highlighter":
                        selected_tool = utils.toggleAction("highlighter")
                    pyautogui.mouseDown()
                    pyautogui.moveTo(clocx, clocy, duration=0.1)
                else:
                    pyautogui.mouseUp()
                    selected_tool = None

            elif fingers == [0, 1, 1, 1, 0]:
                img = utils.displayText("Index, middle & ring up: Eraser mode", img)
                length, _, img = dr.findDistance(index_tip, lmList[12][:2], img)
                if length <= 35:
                    if selected_tool != "eraser":
                        selected_tool = utils.toggleAction("eraser")
                    pyautogui.mouseDown()
                    pyautogui.moveTo(clocx, clocy, duration=0.1)
                else:
                    pyautogui.mouseUp()
                    selected_tool = None

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
finally:
    cap.release()
    cv2.destroyAllWindows()
