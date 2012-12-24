import numpy
import cv
def filter(blue_image, keyer, width=3, orientation='h'):
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

	result_a = result_a.astype(int)
	result_c = result_c.astype(int)

	keyer_filter = numpy.maximum(keyer_a, keyer_c)
	result_b_a = result - result_a
	result_b_c = result - result_c

	result_b_c = result_b_c.astype(numpy.uint8)
	result_b_a = result_b_a.astype(numpy.uint8)

	result = numpy.minimum(result_b_a, result_b_c)
	result = numpy.minimum(result, keyer_filter)
	return result

def filter_for(blue_image, keyer, width=3, orientation='h'):
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
				# temp = min(blue_image[i,j] - blue_image[i-i_shift, j-j_shift], blue_image[i,j] - blue_image[i+i_shift, j+j_shift])
				result[i,j] = temp

	return result
