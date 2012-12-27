import numpy
import math
def general_hough_line(line_image):
	"""
	This function calculates the corresponding hough image, which then can be used to extract lines or to evaluate the match value of a pose.

	parameters:
		-line_image: numpy array, dtype: numpy.float32. This is the output of `line_filter.line_detection_filter(img, keyer)`
	returns:
		-numpy array, dtype: numpy.float32, shape: (360,int(sqrt(line_image.shape[0]**2 + line_image.shape[1]**2)))
	"""
	r_max = int(math.sqrt(line_image.shape[0]**2 + line_image.shape[1]**2))
	result = numpy.zeros((360, r_max), dtype=numpy.float32)

	for x in range(line_image.shape[0]):
		for y in range(line_image.shape[1]):
			value = line_image[x,y]
			impact_value = value/10000.0
			if value > 0:
				for theta in range(0, 360):
					# the real theta
					r_theta = math.radians(theta - 180)
					r = int(y*math.cos(r_theta) + x*math.sin(r_theta))
					result[theta, r] += impact_value

	return result
