import cv2
import mediapipe

cap = cv2.VideoCapture(0)


mpHands = mediapipe.solutions.hands
hands = mpHands.Hands(max_num_hands=1)
mpDraw = mediapipe.solutions.drawing_utils

def main():
    run = True
    while run:
        _, img = cap.read()
        
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        if results.multi_hand_landmarks is not None:           
            mpDraw.draw_landmarks(img, results.multi_hand_landmarks[0], mpHands.HAND_CONNECTIONS)

        flipped = cv2.flip(img, 1)
        cv2.imshow("Image", flipped)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    cap.release()


if __name__ == "__main__":
    main()
