import cv2
from PIL import Image
import urllib.request,io, time
import numpy as np
from matplotlib import pyplot as plt

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm

def randcolors(elemlist):
  for elem in elemlist:
    yield elem, tuple(int(x) for x in list(np.random.choice(range(256), size=3)))

nfeatures = 2000
fastTreshold = 5

path = io.BytesIO(urllib.request.urlopen('http://10.0.0.128/capture').read())
previmg = np.array(Image.open(path).convert('RGB'))
previmg = cv2.rotate(previmg[:,:,::-1], cv2.ROTATE_90_CLOCKWISE) # RBG to BGR
img = previmg

while 1:
  previmg = img
  path = io.BytesIO(urllib.request.urlopen('http://10.0.0.128/capture').read())
  img = np.array(Image.open(path).convert('RGB'))
  img = cv2.rotate(img[:,:,::-1], cv2.ROTATE_90_CLOCKWISE) # RBG to BGR

#  cv2.imshow('capture', img)
#  k = cv2.waitKey(1) & 0xFF
#  if k == 27:
#    break
#  continue

  orb = cv2.ORB_create(nfeatures=nfeatures, fastThreshold=fastTreshold)
  kp1, des1 = orb.detectAndCompute(previmg, None)
  kp2, des2 = orb.detectAndCompute(img, None)

  if len(kp1) == 0 or len(kp2) == 0:
    continue

  desc_matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
  matches = desc_matcher.match(des1,des2)
  matches = sorted(matches, key = lambda x:x.distance)
  if len(matches) < nfeatures / 2 and fastTreshold > 3:
    fastTreshold -= 1
    print('fastTreshold-- (' + str(fastTreshold) + ')')
  if len(matches) == nfeatures:
    fastTreshold += 1
    print('fastTreshold++ (' + str(fastTreshold) + ')')

  vectors = [np.subtract(kp1[m.queryIdx].pt, kp2[m.trainIdx].pt) for m in matches]
  median = normalize(np.median(vectors, axis=0))
  rated = np.array([
    (m, v, (np.dot(normalize(v), median) if np.any(v) else 1)) 
    for m,v in zip(matches, vectors)])
  median_dot = np.median(rated[:,2])
  median_len = np.linalg.norm(np.median(vectors, axis=0))
  mean_len = np.linalg.norm(np.mean(vectors, axis=0))

  good = [r[0] for r in rated if r[2] >= median_dot and abs(np.linalg.norm(r[1]) - median_len) < mean_len]

  img3 = cv2.addWeighted(previmg, 0.5, img, 0.5,0)
  for line, color in randcolors(good):
    p1 = tuple([int(p) for p in kp1[line.queryIdx].pt])
    p2 = tuple([int(p) for p in kp2[line.trainIdx].pt])
    img3 = cv2.line(img3, p1, p2, color, 1)

  cv2.imshow('capture', img3)
  k = cv2.waitKey(100) & 0xFF
  if k == 27:
    break
cv2.destroyAllWindows() # destroys the window showing image