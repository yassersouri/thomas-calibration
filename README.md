Camera Calibration for Soccer Videos
==================

A customized implementation of G.Thomas[2007] paper on calibrating a camera for sports videos like Rugby and Football.

To Do
=====

In a first attempt I want to implement the "Initialization" part of the paper. We already have the camera positions so we do not need to calculate them.

Initialization
--------------

In this paper, rather than attempting to establish the **correspondence** between world world lines and peaks in Hough space, authors use the Hough transform as a means to _quickly_ establish a measure of how well the image **matches** the set of lines that would be expected to be visible from a given pose. A **match value** for a set of lines can be obtained by adding together the set of bins in Hough space that correspond to the lines we are looking for. So testing for a set of _N_ lines is _O(N)_ computationally, which is fast because _N_ is usually less than 20.

They use this _matching_ in an **exhaustive** search process to establish the match value for each pose that we consider. The **speed** of this method must be evaluated.

For each _pre-determined camera position_, the algorithm searches the full range of plausible values of pan, tilt, and field-of-view, calculating the match value.

In this paper (as the only one I've seen) the **curved lines** are represented as a series of line segments. This needs to be tested. Authors used one segment for every 20 degree. So the central circle in the soccer field is represented by 18 line segments. This eliminated the need to handle cureves and lines separately.

Tests
=====

* The speed of initialization.
* Evaluate the assumption that a curved line can be represented by line-segments.

Reference
=========

G.Thomas[2007]: Graham A. Thomas, Real-time camera tracking using sports pitch markings, J. Real-Time Image Processing, 2007.
