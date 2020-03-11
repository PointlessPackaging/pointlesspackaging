import numpy as np
import cv2
import matplotlib.pyplot as plt

import sys

path = 'images/'
inf_addr = 'box_1'
print(sys.argv)
addr = (path+inf_addr+'.jpg') if len(sys.argv) < 2 else (path + sys.argv[1]+'.jpg')


img = cv2.imread(addr)

Z = img.reshape((-1, 3))

# convert to np.float32
Z = np.float32(Z)

# define criteria, number of clusters(K) and apply kmeans()
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 3
ret, label, center = cv2.kmeans(
    Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

# Now convert back into uint8, and make original image
center = np.uint8(center)
res = center[label.flatten()]
res2 = res.reshape((img.shape))


img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# img_gray = res2

# kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
# img_gray = cv2.filter2D(img_gray, -1, kernel)

img_gray = cv2.GaussianBlur(img_gray, (7, 7), 3)
img_gray2 = img_gray.copy()

canvas = np.zeros(shape=img.shape)

edged = cv2.Canny(img_gray, 0, 65)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)

ret, thresh = cv2.threshold(img_gray2, 127, 255, 0)

cnts, hierarchy = cv2.findContours(
    edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


# contours, _ = cv2.findContours(
#     thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(img, cnts, -1, (0, 255, 0), 3)
ddepth = -1
ind = 2
kernel_size = 3 + 2 * (ind % 5)
kernel = np.ones((kernel_size, kernel_size), dtype=np.float32)
kernel /= (kernel_size * kernel_size)

dst = cv2.filter2D(img, ddepth, kernel)

# cnts = cnts[0] if imutils.is_cv2() else cnts[1]
cntsSorted = sorted(cnts, key=lambda x: cv2.contourArea(x), reverse=True)
# cntsSorted = sorted(cnts, key=lambda x: cv2.arcLength(x, True), reverse=True)

""" DRAW CONTOUR IMAGE """
for i, c in enumerate(cntsSorted):
    cv2.drawContours(canvas, c, -1, (255, 255, 255), 2)
    print(cv2.contourArea(c))
    cv2.waitKey(100)
    cv2.imshow('Canny',canvas)

# cv2.imshow("Custom Filter", dst)

# cv2.imshow('', img)
# cv2.imshow('Threshold Contours', thresh)
cv2.imshow('Color Quantization', res2)
cv2.waitKey(0)
cv2.destroyAllWindows()

