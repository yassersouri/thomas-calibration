import numpy

def filter(blue_image, keyer, width=3, orientation='h'):
	"""
	This function implemets the line detection filter.

	parameters:
		-blue_image: numpy array, dtype: numpy.uint8. Is the single channel image as numpy array. In the paper this is the blue componenet of the RGB input image.
			can make this from the single channel CvMat or IplImage: `numpy.fromarray(img)`
		-keyer: numpy array, dtype: numpy.uint8, shape: same as blue_image. This is the chroma keyer output.
		-width: int. is the width of the filter.
		-orientation: 'h' or 'v' for horizontal and vertical respectivly. indicates the direction of the filter.
	returns:
		-numpy array, dtype: numpy.uint8, shape: same as blue_image.
	"""
	result = blue_image

	if orientation == 'h':
		result_a = numpy.roll(result, width, axis=0)
		keyer_a = numpy.roll(keyer, width, axis=0)
		result_c = numpy.roll(result, -1 * width, axis=0)
		keyer_c = numpy.roll(keyer, -1 * width, axis=0)

		result_c[-1*width:, :] = 0
		keyer_c[-1*width:, :] = 0
		result_a[0:width, :] = 0
		keyer_a[0:width, :] = 0

	elif orientation == 'v':
		result_a = numpy.roll(result,width, axis=1)
		keyer_a = numpy.roll(keyer,width, axis=1)
		result_c = numpy.roll(result, -1 * width, axis=1)
		keyer_c = numpy.roll(keyer, -1 * width, axis=1)

		result_c[:, -1*width:] = 0
		keyer_c[:, -1*width:] = 0
		result_a[:, 0:width] = 0
		keyer_a[:, 0:width] = 0
	else:
		raise "orientation is not defined, must be 'h' or 'v'"

	keyer_filter = numpy.maximum(keyer_a, keyer_c)

	# calculate b-a
	temp_b_a = result - result_a
	filter_b_a = numpy.greater(result, result_a) * numpy.uint8(255)
	result_b_a = numpy.minimum(temp_b_a, filter_b_a)

	# calculate b-c
	temp_b_c = result - result_c
	filter_b_c = numpy.greater(result, result_c) * numpy.uint8(255)
	result_b_c = numpy.minimum(temp_b_c, filter_b_c)

	# calculater minimum difference
	result = numpy.minimum(result_b_a, result_b_c)

	# filter with keyer
	result = numpy.minimum(result, keyer_filter)

	# threshold
	filter_output_threshold = 20
	threshold_filter = numpy.greater(result, numpy.uint8(filter_output_threshold)) * numpy.uint8(255)
	result = numpy.minimum(result, threshold_filter)

	return result

def filter_for(blue_image, keyer, width=3, orientation='h'):
	"""
	This function is the much slower version of filter, implemented with for loops.
	At some point I could not find what was wrong with my vectorized implementation so I tried writing it with for loops.
	It actually helped alot. So I'll keep this in the code.
	"""
	result = numpy.zeros(blue_image.shape, dtype=numpy.uint8)

	i_min , j_min = 0,0
	i_max , j_max = blue_image.shape[0], blue_image.shape[1]
	i_shift , j_shift = 0,0

	if orientation == 'h':
		i_min = width
		i_max = blue_image.shape[0] - width
		i_shift = width
	elif orientation == 'v':
		j_min = width
		j_max = blue_image.shape[1] - width
		j_shift = width
	else:
		raise "unknown orientation"

	for i in range(i_min, i_max):
		for j in range(j_min, j_max):
			if keyer[i-i_shift, j-j_shift] or keyer[i+i_shift, j+j_shift]:
				temp1 = 0
				temp2 = 0
				if blue_image[i,j] > blue_image[i-i_shift, j-j_shift]:
					temp1 = blue_image[i,j] - blue_image[i-i_shift, j-j_shift]
				if blue_image[i,j] > blue_image[i+i_shift, j+j_shift]:
					temp2 = blue_image[i,j] - blue_image[i+i_shift, j+j_shift]
				temp = min(temp1, temp2)
				if temp < 20:
					temp = 0
				result[i,j] = temp

	return result
