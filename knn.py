from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import train_test_split
# from imutils import paths
import numpy as np
import argparse
# import imutils
import sys
sys.path.append('/Users/androswong/.virtualenvs/cv/lib/python2.7/site-packages/')
import cv2
import glob, os
from imutils import paths

def convert_img_to_feature_vector(image, size =(32, 32)):
    #flatten image to become a 1-d vector
    return cv2.resize(image, size).flatten()
# def extract_color_histogram(image, bins=(8, 8, 8)):
# 	# extract a 3D color histogram from the HSV color space using
# 	# the supplied number of `bins` per channel
# 	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
# 	hist = cv2.calcHist([hsv], [0, 1, 2], None, bins,
# 		[0, 180, 0, 256, 0, 256])
#
# 	# handle normalizing the histogram if we are using OpenCV 2.4.X
# 	if imutils.is_cv2():
# 		hist = cv2.normalize(hist)
#
# 	# otherwise, perform "in place" normalization in OpenCV 3 (I
# 	# personally hate the way this is done
# 	else:
# 		cv2.normalize(hist, hist)
#
# 	# return the flattened histogram as the feature vector
# 	return hist.flatten()

# initialize the raw pixel intensities matrix and label matrix
rawImages = []
labels = []
motorcycle_image_paths = list(paths.list_images('google_images/motorcycle'))
car_image_paths = list(paths.list_images('google_images/car'))
for (i, imagePath) in enumerate(motorcycle_image_paths):
	# load the image and extract the class label (assuming that our
	# path as the format: /path/to/dataset/{class}.{image_num}.jpg
    image = cv2.imread(imagePath)
    print "INDEX"
    print i
    print "IMAGE"
    print image
    label = 'motorcycle'
    if not image is None:
        pixels = convert_img_to_feature_vector(image)
        rawImages.append(pixels)
        labels.append(label)
for (i, imagePath) in enumerate(car_image_paths):
    image = cv2.imread(imagePath)
    print "INDEX"
    print i
    print "IMAGE"
    print image
    label = 'car'
    if not image is None:
        pixels = convert_img_to_feature_vector(image)
        rawImages.append(pixels)
        labels.append(label)
#use sklearn test split to split in test and training groups
rawImages = np.array(rawImages)
labels = np.array(labels)
(trainRI, testRI, trainRL, testRL) = train_test_split(
	rawImages, labels, test_size=0.25, random_state=42)
print("[INFO] evaluating raw pixel accuracy...")
model = KNeighborsClassifier(n_neighbors= 1,
	n_jobs= -1)
model.fit(trainRI, trainRL)
acc = model.score(testRI, testRL)
print("[INFO] raw pixel accuracy: {:.2f}%".format(acc * 100))
