import numpy as np
import cv2
import matplotlib.pyplot as plt
import sys

path = 'images/'
inf_addr = 'box_1'
print(sys.argv)
addr = (path+inf_addr+'.jpg') if len(sys.argv) < 2 else (path +
                                                         sys.argv[1]+'.jpg')

img = cv2.imread(addr,0)

BINS = 20
np_hist, _ = np.histogram(img, bins=BINS)
print(np_hist)

dmin, dmax, _, _ = cv2.minMaxLoc(img)
if np.issubdtype(img.dtype, 'float'):
    dmax += np.finfo(img.dtype).eps
else:
    dmax += 1

cv_hist = cv2.calcHist([img], [0], None, [BINS], [dmin, dmax]).flatten()

# data = np.reshape(img, (-1, 3))
# print(data.shape)
# data = np.float32(data)

# criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
# flags = cv2.KMEANS_RANDOM_CENTERS
# compactness, labels, centers = cv2.kmeans(data, 1, None, criteria, 10, flags)

# centers[0] = centers[0].astype(int)


# img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# canvas = np.zeros(img.shape)

# img_blur = cv2.GaussianBlur(img, (7,7), 0)

# min_color = np.array(centers[0]-20)
# max_color = np.array(centers[0]+20)

# mask1 = cv2.inRange(img_blur, min_color, max_color)

plt.plot(np_hist, '-', label='numpy')
plt.plot(cv_hist, '-', label='opencv')

plt.legend()
plt.show()
# cv2.imshow('',mask1)
cv2.waitKey(0) 
cv2.destroyAllWindows()
