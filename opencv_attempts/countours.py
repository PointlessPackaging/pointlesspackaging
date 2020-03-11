import numpy as np
import cv2
import matplotlib.pyplot as plt
import sys
import random

path = 'images/'
inf_addr = 'box_1'
print(sys.argv)
addr = (path+inf_addr+'.jpg') if len(sys.argv) < 2 else (path + sys.argv[1]+'.jpg')

img = cv2.imread(addr)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_gray = cv2.GaussianBlur(img_gray, (7, 7), 3)
canvas = np.zeros(img.shape)

canny_edges = cv2.Canny(img_gray, 1, 100)
# canny_edges = cv2.dilate(canny_edges, None, iterations=2)
# canny_edges = cv2.erode(canny_edges, None, iterations=2)

canny_contours, hierarchy = cv2.findContours(canny_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

# cv2.drawContours(canvas, canny_contours, -1, (255, 255, 255), 2)


cntsSorted = sorted(
    canny_contours, key=lambda x: cv2.contourArea(x), reverse=True)
# cntsSorted = sorted(cnts, key=lambda x: cv2.arcLength(x, True), reverse=True)
cnt_max = cv2.contourArea(cntsSorted[0])
""" DRAW CONTOUR IMAGE """
for i, c in enumerate(cntsSorted):
    if 0 < cv2.contourArea(c) <= cnt_max:
        color = random.randint(1, 1000) % 255
        cv2.drawContours(canvas, cntsSorted[i], -1, (color, color, color), 1)
        print("Color:", color, "Area:", cv2.contourArea(c))
        cv2.waitKey(200)
        cv2.imshow('CannyCanvas', canvas)

# cv2.drawContours(img, contours, 5, (0,255,0), 3)

cv2.imshow('',img)
# cv2.imshow('CannyEdges', canny_edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
