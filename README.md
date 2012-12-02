Camera Calibration for Soccer Videos
==================

A customized implementation of G.Thomas[2007] paper on calibrating a camera for sports videos like Rugby ans Football.

To Do
=====

In a first attempt I want to implement the "Initialisation" part of the paper. We already have the camera positions so we do not need to calculate them.

Initialisation
--------------

In this paper, rather than attempting to establish the **correspondence** between world world lines and peaks in Hough space, authors use the Hough transform as a means to _quickly_ establish a measure of how well the image **matches** the set of lines that would be expected to be visible from a given pose. A **match value** for a set of lines can be obtained by adding together the set of bins in Hough space that correspond to the lines we are looking for. So testing for a set of _N_ lines is _O(N)_ computationaly.


Reference
=========

G.Thomas[2007]: Graham A. Thomas, Real-time camera tracking using sports pitch markings, J. Real-Time Image Processing, 2007.
