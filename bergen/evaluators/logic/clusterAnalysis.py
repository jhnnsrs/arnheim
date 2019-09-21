import numpy as np
import cv2
from PIL import Image



def findConnectedCluster(array, size_thresh=2):
    pil_img = Image.fromarray(array)
    pil_img = np.uint8(pil_img)
    numpy_image = np.array(pil_img)
    img = cv2.cvtColor(numpy_image, cv2.COLOR_GRAY2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    n_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh)

    numbercluster = 0
    for i in range(1, n_labels):
        if stats[i, cv2.CC_STAT_AREA] >= size_thresh:
            # print(stats[i, cv2.CC_STAT_AREA])
            x = stats[i, cv2.CC_STAT_LEFT]
            y = stats[i, cv2.CC_STAT_TOP]
            w = stats[i, cv2.CC_STAT_WIDTH]
            h = stats[i, cv2.CC_STAT_HEIGHT]
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), thickness=1)
            numbercluster += 1

    return (img, numbercluster)