import cv

def get_blue_component(img):
	"""
	This functions returns only the blue component of an RGB color image.

	parameters:
		-img: CvMat, type: CV_8UC3 RGB color image.
	returns:
		-CvMat, type: CV_8UC1, same size as `img` 
	"""
	blue_component = cv.CreateMat(img.rows, img.cols, cv.CV_8UC1)
	cv.Split(img, blue_component, None, None, None)

	return blue_component
