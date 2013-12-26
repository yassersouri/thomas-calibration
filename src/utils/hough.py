# coding=utf8
import numpy
import math

IMPACT_CONST = 1/10000.0

def general_hough_line(line_image):
	"""
	This function calculates the corresponding hough image, which then can be used to extract lines or to evaluate the match value of a pose.

	parameters:
		-line_image: numpy array, dtype: numpy.float32. This is the output of `line_filter.line_detection_filter(img, keyer)`
	returns:
		-numpy array, dtype: numpy.float32, shape: (270,int(sqrt(line_image.shape[0]**2 + line_image.shape[1]**2)))
	"""

	r_max = int(math.sqrt(line_image.shape[0]**2 + line_image.shape[1]**2))
	result = numpy.zeros((270, r_max), dtype=numpy.float32)

	for x in range(line_image.shape[0]):
		for y in range(line_image.shape[1]):
			value = line_image[x,y]
			impact_value = value * IMPACT_CONST
			if value > 0:
				for theta in range(0, 270):
					# the real theta
					r_theta = math.radians(theta - 90)
					r = int(y*math.cos(r_theta) + x*math.sin(r_theta))
					result[theta, r] += impact_value

	return result

def spatialised_hough_line(line_image, S=10):
	"""
	This function calculates the corresponding spatialised hough image, which then can be used to evaluate the match value of a pose.

	parameters:
		-line_image: numpy array, dtype: numpy.float32. This is the output of `line_filter.line_detection_filter(img, keyer)`
		-S: int, number of segments for the spatialised hough transform
	returns:
		-list of size `S` of numpy array, dtype: numpy.float32, shape: (270,int(sqrt(line_image.shape[0]**2 + line_image.shape[1]**2)))
	"""
	r_max = int(math.sqrt(line_image.shape[0]**2 + line_image.shape[1]**2))
	# allocate memory
	result = [0] * S
	for i in range(S):
		result[i] = numpy.zeros((270, r_max), dtype=numpy.float32)

	# some constants
	_3pi_4 = -3 * math.pi / 4 # -3π / 4
	_pi_4 = -1 * math.pi / 4  # - π / 4
	pi_4 = -1 * -_pi_4        #   π / 4
	__3pi_4 = -1 * _3pi_4     #  3π / 4

	horizontal_subbin_width = int((line_image.shape[0] - 1)/S) + 1
	vertical_subbin_width = int((line_image.shape[1] - 1)/S) + 1

	for x in range(line_image.shape[0]):
		for y in range(line_image.shape[1]):
			value = line_image[x,y]
			impact_value = value * IMPACT_CONST
			if value > 0:
				for theta in range(0, 270):
					# the real theta
					r_theta = math.radians(theta - 90)
					r = int(y*math.cos(r_theta) + x*math.sin(r_theta))
					if (r_theta > _3pi_4 and r_theta < _pi_4) or (r_theta > pi_4 and r_theta < __3pi_4):
						# the line is horizontal
						# decide based on x and height
						sub_hough_num = int(x/horizontal_subbin_width)
					else:
						# the line is vertical
						# decide based on y and width
						sub_hough_num = int(y/vertical_subbin_width)
					result[sub_hough_num][theta, r] += impact_value
	return result