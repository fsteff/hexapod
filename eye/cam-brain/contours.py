import cv2
from PIL import Image
import urllib.request,io, time, math
import numpy as np
from matplotlib import pyplot as plt

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm

colorlist = [tuple(int(x) for x in list(np.random.choice(range(256), size=3))) for i in range(1000)]

min_tres = 10
max_tres = 220

path = io.BytesIO(urllib.request.urlopen('http://10.0.0.128/capture').read())
previmg = np.array(Image.open(path).convert('RGB'))
previmg = cv2.rotate(previmg, cv2.ROTATE_90_CLOCKWISE) # RBG to BGR
img = previmg

while 1:
  previmg = img
  path = io.BytesIO(urllib.request.urlopen('http://10.0.0.128/capture').read())
  img = np.array(Image.open(path).convert('RGB'))
  img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE) # RBG to BGR

  mask1 = cv2.Canny(previmg, min_tres, max_tres)
  cnts1 = cv2.findContours(mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  mask2 = cv2.Canny(img, min_tres, max_tres)
  cnts2 = cv2.findContours(mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  
  cnts1 = np.array(cnts1[0]).flatten()
  cnts2 = np.array(cnts2[0]).flatten()

#  canny = img.copy()
#  for idx, cnt in enumerate(cnts1):
#    color = colorlist[idx]
#    canny = cv2.fillPoly(canny, [cnt], color)
#  canny = cv2.imshow('img1', canny)

  centers1 = [np.median(cnt, axis=0) for cnt in cnts1]
  centers2 = [np.median(cnt, axis=0) for cnt in cnts2]

  # TODO: better similarity measures, this one is garbage (Does not account size)
  similarity = np.zeros((len(cnts1), len(cnts2)))
  for i1 in range(len(cnts1)):
    for i2 in range(len(cnts2)):
      similarity[i1, i2] = cv2.matchShapes(cnts1[i1], cnts2[i2], 1, 0)

  closeness = np.zeros((len(centers1), len(centers2)))
  for i1 in range(len(centers1)):
    for i2 in range(len(centers2)):
      closeness[i1, i2] = np.sum(np.linalg.norm(centers1[i1] - centers2[i2]))

  mediandist = np.median(closeness)
  #maxdist = np.max(closeness)
  #for i1 in range(len(centers1)):
  #  for i2 in range(len(centers2)):
  #    if closeness[i1, i2] > mediandist:
  #      similarity[i1, i2] += 1/maxdist

  indices = [row.argmin() for row in similarity]

  #cnts1 = [cv2.convexHull(cnt, True) for cnt in cnts1]
  #cnts2 = [cv2.convexHull(cnt, True) for cnt in cnts2]

  pairs = [(cnts1[i1], cnts2[i2]) 
    for i1, i2 in enumerate(indices) 
    if similarity[i1, i2] < 0.5 
      and closeness[i1, i2] > img.shape[0] * 0.05
      and closeness[i1, i2] < img.shape[0] * 0.1
      and len(cnts1[i1]) > 4 
      and len(cnts2[i2]) > 4]

  img3 = cv2.addWeighted(previmg, 0.5, img, 0.5,0)
  for idx, pair in enumerate(pairs):
    color = colorlist[int(np.mean(pair[0][:,0,0]) / img3.shape[0] * len(colorlist))]
    img3 = cv2.polylines(img3, [pair[0]], True, color, 2)
    img3 = cv2.polylines(img3, [pair[1]], True, color, 2)

  cv2.imshow('matches', img3)
  k = cv2.waitKey(5) & 0xFF
  if k == 27:
    break
cv2.destroyAllWindows() # destroys the window showing image