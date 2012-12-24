Camera Calibration for Soccer Videos
==================

A customized implementation of G.Thomas[2007] paper on calibrating a camera for sports videos like Rugby and Football.

Description
===========

In a first attempt I want to implement the "Initialization" part of the paper. We already have the camera positions so there is no problem starting from here.

Initialization
--------------

In this paper, rather than attempting to establish the **correspondence** between world lines and peaks in Hough space, author uses the Hough transform as a means to *quickly* establish a measure of how well the image **matches** the set of lines that would be expected to be visible from a given pose. A **match value** for a set of lines can be obtained by adding together the set of bins in Hough space that correspond to the lines we are looking for. So testing for a set of *N* lines is *O(N)* computationally, which is fast because *N* is usually less than 20.

They use this *matching* in an **exhaustive** search process to establish the match value for each pose that we consider. The **speed** of this method must be evaluated.

For each *pre-determined camera position*, the algorithm searches the full range of plausible values of pan, tilt, and field-of-view, calculating the match value.

In this paper (as the only one I've seen) the **curved lines** are represented as a series of line segments. This needs to be tested. Author used one segment for every 20 degree. So the central circle in the soccer field is represented by 18 line segments. This eliminated the need to handle curves and lines separately, and thus simplifies the implementation.

### Line detection filter

Author designed the line detection filter assuming that we know the orientation (vertical vs horizontal) and width of the line that we want to filter out. But in reality we do *not* know the orientation and width of the line, thus we apply this filter with several width size and orientation combinations and add their output together.

The filter is designed so that it will ignore regions which are significantly wider that a pitch line. The filter is applied either horizontally or vertically. The width thus needs to be adjusted to reflect the its *width in the horizontal or vertical direction* as appropriate. The **local maximum** of the filter output is taken to identify *a pixel at the center of the line*.

The filter is applied to the **blue** component of the image.

The adjacent pixels must also have a color in the range expected for grass. For this the author suggests using a hue-based chroma-keyer. The keyer needs to merely indicate areas unlikely to be grass, so that immediately adjacent areas are not considered as possible lines.

### The variant of Hough transform - Spatialised Hough transform

A variant of Hough transform is used that maintains some of the spatial information. Because the peak in the Hough transform from a short line segment (or a curve line segment) may be no higher than a peak caused by samples from several other line segments and from the limbs of a player, that coincidentally happen to be co-linear. Thus short line segments may be incorrectly inferred. The catch is that information that caused the genuine peak came from samples in a specific localized area, whilst the other came from a spatially diverse area.

**How to retain spatial information in Hough transform?** Simply divide the image into S 1D segments. This maintains a common set of bins for the whole image, with each bin being sub-divided into S sections. For simplicity we divide the line by reference to either the horizontal portion of the image in which it lies (for lines that are closer to horizontal than vertical (?)), or the vertical portion (for lines that are closer to vertical).

Thus to determine the sub-bin that a given pixel contributes to, it is only necessary to check its *x* or *y* coordinate, depending on the angle that the bin in the transform corresponds to.

The resulting Hough space has 3 dimensions: distance and angle (as in a conventional Hough transform) and *distance from picture edge*, measured from either bottom or left edge of the picture frame depending on the slope of the line. This third axis (distance from picture edge) has length S.

The catch is that both vertical and horizontal are divided into S sub-regions, so upper and left sections have a *common* sub-Hough. Also not all lines use all sub-Houghs. But since memory is not an issue for now, and this method is really quick and simple, we will stick with this. If we add together all the sub-Houghs we get a conventional Hough transform.

**How to use the line detection filter?** The line detection filter assumes that we know the *orientation* and *width* of the lines, which we do not! With a range of assumed line widths, and using both the vertical and horizontal direction, we apply the filter to the image several times. We add the outputs together, then for each pixel which is more than a **threshold**, we add a value to the appropriate sub-bins **proportional** to the summed output of the line detection filter.

Implementation
--------------

### Step 1

Use the line detection output with several parameters and calculate the spatialised hough transform.

### Step 2

Search the possible values of pan, tilt and zoom for a *specific camera position*. For each plausible value of pan, tilt and zoom, project the lines of the pitch model into the image. The **step size** for search is set to be equivalent to a fixed number of pixels in the image (?).

For each **candidate pose** that *at least 3 lines are visible*, we compute the list of sub-bins that correspond to visible lines, add their contents together to get the match score of this pose. We **ignore poses** close to other poses with a higher match value, as they are not useful local maxima.

**How to speed up the search?** As the set of sub-bins to be used for each camera pose only depends on camera position and pitch model, this list can be pre-computed for a specific camera position and thus significantly increase the search speed.

The set of 5 to 10 best poses are used in step 3.

### Step 3

The third step is tracking which we are not concerned with right now.

Tests
=====

* The speed of initialization.
* Evaluate the assumption that a curved line can be represented by line-segments.
* Evaluate the effect of including curved lines as line segments versus completely eliminating them.
* Evaluate the effect of the spatial Hough transform versus regular Hough transform.
* The line detection filter used is complicated and time consuming. What is the effect of changing this filter to a simpler filter.

### Blue component

Does blue component of the image distinguish well between the green grass and the white line? - Yes it does. Certainly you don't want the green component! Below you see the blue component.
![Blue Component](https://raw.github.com/yassersouri/thomas-calibration/master/docs/f581_4_1_blue.jpg)

### Effect of chroma keyer on line detection output

Below you can see the output of using the chroma keyer on the output of the line detection filter.

**With Chroma Keyer**:

![]()

**Without Chroma Keyer**:

![]()

As you can see, when not using the chroma keyer there are lots of noise in the output of the line detection filter, spatially in area of crowd in the stadium.

Questions
=========
**Q:** How do we know if a line in the image is closer to horizontal or vertical?  - **A:** When calculating the Hough transform, each pixel in the frame space, corresponds to a set of bins in the Hough space. According to the angle that the bin corresponds to we can decide whether the line is more horizontal or more vertical, then by checking its *x* or *y* coordinates we decide which sub-Hough space we should use.

**Q:** I have no idea why applying the line detection filter several times and then adding their outputs together makes sense! Why first design a powerful line detection filter with orientation and line width parameters, and then add together output of the filter for different values of its parameters blindly?

**Q:** How is the step size determined in the search step? It is set to be equivalent to a fixed number of pixels in the image, but the fixed number of pixels seems to change with equal increase in zoom value. In the paper the author says for zoom consider the motion caused at the edge of the image.

Tasks
=====
* ~~Implement line detection filter.~~
* Implement the spatialised Hough transform described in the paper.
* Implement the search algorithm for initialization.

Code
====
The code is written in Python 2.7.

Dependencies:

* OpenCV 2 with python bindings.
* numpy >= 1.6

Hight leven details:

* I've used [CvMat](http://opencv.willowgarage.com/documentation/python/core_basic_structures.html#cvmat) for images. So utility codes work with that data structure. Although some utility functions work with numpy arrays.
* I've tried my best to prevent using `for` loops in code.

### To Do

* cleanup code for hue based chroma keyer.
* write comment for `line_filter`.
* test the overflow error on the chroma keyer.


Notice
======
This work is done by [Yasser Souri](http://ce.sharif.ir/~souri) in collaboration with Mehran Fotouhi in [Image Processing Laboratory (IPL)](http://ipl.ce.sharif.edu/), [Computer Engineering Department](http://ce.sharif.ir/) in [Sharif University of Technology](http://sharif.ir/), under supervision of [Prof. Shohreh Kasaei](http://sharif.edu/~skasaei/).

Some parts of the "Description" section is copied from the G.Thomas[2007] paper.

Images in `images` directory are copy righted. Academic or non-academic use requires permission from Image Processing Laboratory in Sharif University. If you cite our work, it is basically OK for academic use, but asking for permission is needed.

Reference
=========

G.Thomas[2007]: Graham A. Thomas, Real-time camera tracking using sports pitch markings, J. Real-Time Image Processing, 2007.

Contact
=======
For inquiries regarding the implementation and licensing please contact Yasser Souri:

	Image Processing Laboratory (IPL)
    Room 822, Computer Engineering Department
    Sharif University of Technology
    yassersouri@gmail.com
    souri@ce.sharif.edu