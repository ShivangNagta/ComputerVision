import cv2
import mediapipe
import pygame
import math
from sand import Grid
import numpy as np


WIDTH = 600
HEIGHT = 600
win = pygame.display.set_mode((WIDTH, HEIGHT))

cap = cv2.VideoCapture(0)

mpHands = mediapipe.solutions.hands
hands = mpHands.Hands(max_num_hands=10)
mpDraw = mediapipe.solutions.drawing_utils

def get_next_point(x, y, angle, length):
    x2 = x + math.sin(angle) * length
    y2 = y + math.cos(angle) * length
    return x2, y2


def mean(data):
    return sum(data) / len(data)


def map_range(value, in_min, in_max, out_min, out_max):
    in_range = in_max - in_min
    out_range = out_max - out_min
    percent_done = (value - in_min) / in_range
    return out_range * percent_done + out_min


def get_hand_location(img):
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks is not None:
        x_values = []
        y_values = []
        for hand in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, hand, mpHands.HAND_CONNECTIONS)
            for identity, landmark in enumerate(hand.landmark):
                # print(identity, landmark)
                height, width, channels = img.shape
                centerx, centery = int(landmark.x * width), int(landmark.y * height)

                x_values.append(centerx)
                y_values.append(centery)

                # if identity == 1:
                #    cv2.circle(img, (centerx, centery), 10, (255,0,255), cv2.FILLED)
        meanx = int(mean(x_values))
        meany = int(mean(y_values))
        variation = int(np.var(y_values))
        return meanx, meany, variation






def main():
    run= True
    clock= pygame.time.Clock()
    
    sandbox= Grid()
    clock.tick(200)
    while run:
        T = 4
        success, img = cap.read()
        win.fill((25,25,25))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        hand_location = get_hand_location(img)
        if hand_location is not None:
            if hand_location[2] > 1000:     
                sandbox.addSand((WIDTH - hand_location[0]) - (WIDTH - hand_location[0])% T, hand_location[1] - hand_location[1]%T)
                sandbox.update_position()
                sandbox.draw(win)
                pygame.display.flip()
                flipped= cv2.flip(img, 1)
                cv2.imshow("Image", flipped) 
            elif hand_location[2] < 1000:
                for _ in range(4):
                    sandbox.addSand((WIDTH - hand_location[0]) - (WIDTH - hand_location[0])% T, hand_location[1] - hand_location[1]%T)
                    sandbox.addSand(((WIDTH - hand_location[0]) - (WIDTH - hand_location[0])% T)-1, hand_location[1] - hand_location[1]%T)
                    sandbox.addSand(((WIDTH - hand_location[0]) - (WIDTH - hand_location[0])% T)+1, (hand_location[1] - hand_location[1]%T)+2)
                    sandbox.addSand(((WIDTH - hand_location[0]) - (WIDTH - hand_location[0])% T)-2, (hand_location[1] - hand_location[1]%T)-1)
                    sandbox.addSand(((WIDTH - hand_location[0]) - (WIDTH - hand_location[0])% T)+2, (hand_location[1] - hand_location[1]%T)+1)
                    sandbox.addSand(((WIDTH - hand_location[0]) - (WIDTH - hand_location[0])% T)+3, (hand_location[1] - hand_location[1]%T))
                sandbox.update_position()
                sandbox.draw(win)
                pygame.display.flip()
                flipped= cv2.flip(img, 1)
                cv2.imshow("Image", flipped) 
                    
            
        else:
            sandbox.update_position()
            sandbox.draw(win)
            pygame.display.flip()
            flipped= cv2.flip(img, 1)
            cv2.imshow("Image", flipped)
                   
        pygame.display.update()
    
if __name__ == "__main__":
    main()

cv2.destroyWindow("Image")
pygame.quit()