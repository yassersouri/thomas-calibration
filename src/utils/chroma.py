import cv
import math
import numpy

def degree_to_2pi(theta):
	while theta >= 360:
		theta -= 360
	return theta

def hue_keyer(img, theta=120, acceptance_angle=90):
	# theta = degree_to_2pi(theta)
	LB = (theta - acceptance_angle)
	UB = (theta + acceptance_angle)

	result = cv.CreateMat(img.rows, img.cols, cv.CV_8UC1)

	img_HSV = cv.CreateMat(img.rows, img.cols, cv.CV_8UC3)
	cv.CvtColor(img, img_HSV, cv.CV_RGB2HSV)

	img_HSV_array = numpy.asarray(img_HSV)
	result_array = numpy.asarray(result)

	# print (img_HSV_array[:,:,0] > LB) & (img_HSV_array[:,:,0] < UB)
	# exit()
	result_array[(img_HSV_array[:,:,0] > LB) & (img_HSV_array[:,:,0] < UB)] = 255

	return result_array


def chroma_keyer(img, theta=170, acceptance_angle=150):
	"""
	Computes the chroma keyer output of an image, given the hue angle and acceptance angle.

	parameters:
		-img: CvMat, type: CV_8UC3 RGB color image.
		-theta: int, hue of the typical color that needs to be accepted as foreground, in degrees.
		-acceptance_angle: int, the constant that determines the acceptance angle.
			acceptance_angle = 2 * arctan(1/a)
			a = 1/tan(acceptance_angle/2)
	returns:
		-CvMat, type: CV_8UC1, same size as `img`. At each pixel is either 0 (for background) or 1 (for foreground)
	"""
	# define constants
	FOREGROUND = 255
	BACKGROUND = 0

	# allocate memory for output.
	result = cv.CreateMat(img.rows, img.cols, cv.CV_8UC1)

	# convert image to YCbCr space
	img_YCbCr = cv.CreateMat(img.rows, img.cols, cv.CV_8UC3)
	cv.CvtColor(img, img_YCbCr, cv.CV_RGB2YCrCb)

	# convert theta to radians
	theta = math.radians(theta)
	acceptance_angle_2 = math.radians(acceptance_angle/2.0)
	# calculate the acceptance constant
	a = 1.0 / math.tan(acceptance_angle_2)

	for x in range(img.rows):
		for y in range(img.cols):
			Y,Cr,Cb = img_YCbCr[x,y]
			Cr -= 128
			Cb -= 128
			X = Cb * math.cos(theta) + Cr * math.sin(theta)
			Z = Cr * math.sin(theta) - Cr * math.cos(theta)
			K = X - a * abs(Z)
			if K > 0:
				result[x,y] = FOREGROUND
			else:
				result[x,y] = BACKGROUND

	return result