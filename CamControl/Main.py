import cvzone, time, cv2
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Key, Controller

#CONFIG, Change accordingly. hand_detect_difference according to your camera's distance from hand.
hand_detect_difference = 45 #INCREASE TO MAKE IT DETECT LESS MOVEMENT, More if it wrongly detects.
delay = 1.2 #delay for while loop after command to not accidently run while closing your hand after movement.
confidence = 0.6 #Confidence level of hand required to be detected , (0.1 - 0.9).

time.sleep(3)
keyboard = Controller()
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, capture.get(cv2.CAP_PROP_FRAME_WIDTH)) 
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

detector = HandDetector(detectionCon=confidence, maxHands=1, minTrackCon=confidence)
hand1pos = [0,0,0]
fpsReader = cvzone.FPS()
oldFingerCount = 0


while True:
    success, image = capture.read()
    hands, image = detector.findHands(image, draw=True)
    
    if hands:
        fps, image = fpsReader.update(image,pos=(50,80),color=(0,255,0),scale=5,thickness=5)
        
        hand1 = hands[0]
        lmList1 = hand1["lmList"]
        hand1pos2 = detector.findPosition(image=image, handNo=0)
        hand1pos2 = hand1pos2[3]
        fingers1 = detector.fingersUp(hands[0])
        finger1count = fingers1.count(1)
        centerpoint1 = hand1["center"]
        if hand1pos2[2] > hand1pos[2] + hand_detect_difference and not hand1pos[2] == 0 and finger1count >= 4 and oldFingerCount >= 4:
            keyboard.press(Key.down)
            keyboard.release(Key.down)
            time.sleep(delay)
        elif hand1pos2[2] < hand1pos[2] - hand_detect_difference and not hand1pos[2] == 0 and finger1count >= 4 and oldFingerCount >= 4:
            keyboard.press(Key.up)
            keyboard.release(Key.up)
            time.sleep(delay)
        
        
        elif hand1pos2[1] > hand1pos[1] + hand_detect_difference and not hand1pos[1] == 0 and finger1count >= 4 and oldFingerCount >= 4:
            keyboard.press(Key.left)
            keyboard.release(Key.left)           
            time.sleep(delay)
        elif hand1pos2[1] < hand1pos[1] - hand_detect_difference and not hand1pos[1] == 0 and finger1count >= 4 and oldFingerCount >= 4:
            keyboard.press(Key.right)
            keyboard.release(Key.right)
            time.sleep(delay)
        
        elif finger1count == 3 and oldFingerCount == 3:
            keyboard.press(Key.esc)
            keyboard.release(Key.esc)
            time.sleep(delay)
        elif finger1count == 2 and oldFingerCount == 2:
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            time.sleep(delay)
        print("Fingercount:", finger1count, oldFingerCount)
        oldFingerCount = finger1count
        
        #don't move variables upwards, it stops working
        hand1pos = detector.findPosition(image=image, handNo=0)
        hand1pos = hand1pos[3]

        if len(hands) == 2:
            hand2pos = detector.findPosition(image=image, handNo=1)
            hand2pos = hand2pos[3]
            hand2 = hands[1]
            lmList2 = hand2["lmList"]
            bbox2 = hand2["bbox"]
            centerpoint2 = hand2["center"]
            handtype2 = hand2["type"]
            fingers2 = detector.fingersUp(hand2)
            finger2count = fingers2.count(1)

 