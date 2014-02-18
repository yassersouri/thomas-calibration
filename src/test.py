import cv
import numpy
from datetime import datetime

from utils import color
from utils import chroma
from utils import line_filter
from utils import hough

import lib.PCPM

def main():
	folder = '../images/'
	image = 'f581_4_1'
	# image = 'f1098_2_1'
	# image = 'test'
	# image = 'f00166'
	# image = 'f00378'
	image_ext = '.jpg'
	# image_ext = '.png'

	print lib.PCPM.projmatrix(6581.683679,1072.853995,969.786074,
        2.4474, -0.0416, -0.1467
        ,286.820329582749,-1528.34592002449,2392.43585096462
        , 0.000156, 1.0001042808)
	exit()

	img = cv.LoadImageM(folder + image + image_ext)

	a = datetime.now()

	bi = color.get_blue_component(img)
	bi_array = numpy.asarray(bi)

	# for i in range(30):
	# keyer = chroma.chroma_keyer(img, theta=225, acceptance_angle=10)
	keyer = chroma.hue_keyer(img, theta=110.0*255/360, acceptance_angle=20)

	# lines = line_filter.filter_line(bi_array, numpy.asarray(keyer), width=5, orientation='h')
	lines = line_filter.line_detection_filter(bi_array, numpy.asarray(keyer))

	# g_hough = hough.general_hough_line(lines)
	s_hough = hough.spatialised_hough_line(lines, S=10)

	b = datetime.now()
	print (b-a)

	cv.ShowImage('orig', img)
	cv.ShowImage('blue', bi)
	cv.ShowImage('keyer', cv.fromarray(keyer))
	cv.ShowImage('lines', cv.fromarray(lines))
	# cv.ShowImage('hough', cv.fromarray(g_hough))
	for i in range(10):
		# cv.ShowImage('hough' + str(i), cv.fromarray(s_hough[i]))
		pass

	# cv.SaveImage(folder + image + '_blue' + image_ext, bi)
	# cv.SaveImage(folder + image + '_output_with' + image_ext, cv.fromarray(lines))

	cv.WaitKey(0)

if __name__ == '__main__':
	main()