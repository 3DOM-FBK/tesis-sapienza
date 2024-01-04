import numpy as np
import sys, os
import cv2

colors = [
     (255, 0 , 0),
     (0, 255 , 0),
     (0, 0 , 255),
     (255, 255 , 0),
     (255, 0 , 255),
     (0, 255 , 255),
     (0, 120 , 200)
]

image = cv2.imread("data/test.png")
out = np.zeros(image.shape)

for i, color in enumerate(colors):

    mask = cv2.inRange(image, color, color)

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # Trovo contorni    

    for contour in contours:
        epsilon = 0.0001 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, closed=True)
        approx = np.squeeze(approx, axis=1)

        cv2.polylines(out, [approx], True, color, 7)
    
cv2.imwrite(f"data/contours.png", out)

# per ogni classe 
#     creo maschera b/w con con i pixel del colore classe

#     faccio find contours per separare i vari blob

#     per ogni contour faccio ApproxPolyDP