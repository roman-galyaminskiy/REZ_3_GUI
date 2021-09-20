import cv2
import matplotlib.pyplot as plt
import numpy as np
import time
from scipy.spatial.distance import cityblock
from scipy.spatial.distance import euclidean

WINDOW_SIZE = 100
STEP_SIZE = 10
IMAGE_PATH = "screenshot.png"

img = cv2.imread(IMAGE_PATH, cv2.IMREAD_GRAYSCALE)


hist_array = []
for x in range(0, img.shape[1] - WINDOW_SIZE, STEP_SIZE):
   for y in range(0, img.shape[0] - WINDOW_SIZE, STEP_SIZE):
      # Используем маску в качестве скользящего окна
      mask = np.zeros(img.shape[:2], np.uint8)
      mask[x:x+WINDOW_SIZE,y:y+WINDOW_SIZE] = 255
      masked_img = cv2.bitwise_and(img,img,mask = mask)
      hist_mask = cv2.calcHist([img],[0],mask,[256],[0,256])
      hist_array.append([[x, y], hist_mask])
      # Закомментированные строки ниже использовались для отрисовки красивой картинки
      # cv2.imshow("Window", masked_img)
      # cv2.waitKey(1)
      # time.sleep(0.025)

min_euclidean_dist = [-1, [], []]
min_manhattan_dist = [-1, [], []]

for i in range(len(hist_array)):
   for j in range(len(hist_array)):
      if (i != j):
         if (min_euclidean_dist[0] == -1):
            min_euclidean_dist = [
               # Применял cv2.norm(hist1, hist2, normType=cv2.NORM_L2)
               # кажется, работало быстрее
               euclidean(hist_array[i][1], hist_array[j][1]),
               hist_array[i],
               hist_array[j]
            ]

            min_manhattan_dist = [
               cityblock(hist_array[i][1], hist_array[j][1]),
               hist_array[i],
               hist_array[j]
            ]
         
         else:
            dist = euclidean(hist_array[i][1], hist_array[j][1])
            if (min_euclidean_dist[0] > dist):
               min_euclidean_dist = [
                  dist,
                  hist_array[i],
                  hist_array[j]
               ]

            dist = cityblock(hist_array[i][1], hist_array[j][1])
            if (min_manhattan_dist[0] > dist):
               min_manhattan_dist = [
                  dist,
                  hist_array[i],
                  hist_array[j]
               ]

print(min_euclidean_dist[0]), min_manhattan_dist[0])
