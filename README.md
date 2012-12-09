Camera Calibration for Soccer Videos
==================

A customized implementation of G.Thomas[2007] paper on calibrating a camera for sports videos like Rugby and Football.

Description
===========

In a first attempt I want to implement the "Initialization" part of the paper. We already have the camera positions so there is no problem starting from here.

Initialization
--------------

In this paper, rather than attempting to establish the **correspondence** between world world lines and peaks in Hough space, authors use the Hough transform as a means to _quickly_ establish a measure of how well the image **matches** the set of lines that would be expected to be visible from a given pose. A **match value** for a set of lines can be obtained by adding together the set of bins in Hough space that correspond to the lines we are looking for. So testing for a set of _N_ lines is _O(N)_ computationally, which is fast because _N_ is usually less than 20.

They use this _matching_ in an **exhaustive** search process to establish the match value for each pose that we consider. The **speed** of this method must be evaluated.

For each _pre-determined camera position_, the algorithm searches the full range of plausible values of pan, tilt, and field-of-view, calculating the match value.

In this paper (as the only one I've seen) the **curved lines** are represented as a series of line segments. This needs to be tested. Authors used one segment for every 20 degree. So the central circle in the soccer field is represented by 18 line segments. This eliminated the need to handle curves and lines separately, and thus simplifies the implementation.

### The variant of Hough transform - Spatialised Hough Transform

A variant of Hough transform is used that maintains some of the spatial information. Because the peak in the Hough transform from a short line segment (or a curve line segment) may be no higher than a peak caused by samples from several other line segments and from the limbs of a player, that coincidentally happen to be co-linear. Thus short line segments may be incorrectly inferred. The catch is that information that caused the genuine peak came from samples in a specific localized area, whilst the other came from a spatially diverse area.

**How to retain spatial information in Hough transform?** Simply divide the image into S 1D segments. This maintains a common set of bins for the whole image, with each bin being sub-divided into S sections (?). For simplicity we divide the line by reference to either the horizontal portion of the image in which it lies (for lines that are closer to horizontal than vertical (?)), or the vertical portion (for lines that are closer to vertical).

Thus to determine the sub-bin that a given pixel contributes to, it is only necessary to check its _x_ or _y_ coordinate, depending on the angle that the bin in the transform corresponds to.

The resulting Hough space has 3 dimensions: distance and angle (as in a conventional Hough transform) and _distance from picture edge_, measured from either bottom or left edge of the picture frame depending on the slope of the line. This third axis (_distance from picture edge_) has length S.

The catch is that both vertical and horizontal are divided into S sub-regions. Also not all lines use all sub-Houghs. But since memory is not an issue for now, and this method is really quick and simple, we will stick with this.



Tests
=====

* The speed of initialization.
* Evaluate the assumption that a curved line can be represented by line-segments.
* Evaluate the effect of including curved lines as line segments versus completely eliminating them.
* Evaluate the effect of the spatial Hough transform versus regular Hough transform.

Questions
=========
**Q:** How does sub-dividing an image into S 1D section maintains a common set of bins? I can't figure this out right now!

**A:** ?

**Q:** How do we know if a line in the image is closer to horizontal or vertical? 

**A:** When calculating the Hough transform, each pixel in the frame space, corresponds to a set of bins in the Hough space. According to the angle that the bin corresponds to we can decide whether the line is more horizontal or more vertical, then by checking its _x_ or _y_ coordinates we decide which sub-Hough space we should use.


Tasks
=====
* Implement line pixel detection.
* Implement the spatialised Hough transform described in the paper.

Notice
======
This work is done by Yasser Souri in [Image Processing Labratory (IPL)](http://ipl.ce.sharif.edu/), [Computer Engineering Department](http://ce.sharif.ir/) in [Sharif University of Technology](http://sharif.ir/), under supervision of [Prof. Shohreh Kasaei](http://sharif.edu/~skasaei/).

Some parts of the "Description" section is copied from the G.Thomas[2007] paper.


Reference
=========

G.Thomas[2007]: Graham A. Thomas, Real-time camera tracking using sports pitch markings, J. Real-Time Image Processing, 2007.
