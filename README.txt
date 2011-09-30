README.txt
<brussell@csail.mit.edu>
<torralba@csail.mit.edu>
Created: 01/19/2006
Updated: 07/01/2009

Here you will find the source code to install the LabelMe annotation
tool on your server. LabelMe is an annotation tool writen in
Javascript for online image labeling. The advantage with respect to
traditional image annotation tools is that you can access the tool
from anywhere and people can help you to annotate your images without
having to install or copy a large dataset onto their computers.

REQUIREMENTS:

You will need the following to set up the LabelMe tool on your web
server:

* Run an Apache server on a Linux system (we have not tested the
  system on Windows; if you can set this up on Windows, please let us
  know).
* Enable authconfig in Apache so that server side includes (SSI) will
  work.  This will allow SVG drawing capabilities.
* Allow perl/CGI scripts to run.

INSTALLATION:

You will need to make the following directories:

1. Images
2. Annotations
3. TmpAnnotations

Insert the images that you wish to label in "Images". The images must
be organized into subdirectories (e.g.,
Images/folder1/*.jpg). Currently, we do not support multiple directory
levels. The corresponding subdirectories should also be created in the
Annotations folder.

Set the images to have read permissions on your web server and folders
in the "Annotations" folder to have write permissions.  Also,
"TmpAnnotations" needs to have write permissions.

Modify the "Makefile" variables "IMAGES_DIR" and "ANNOTATIONS_DIR" to
point to the above directories.  Now, run "make".  This will set up
LabelMe.

To use the tool, open in your browser: http://yourserver.edu/tool.html

If you are not able to draw polygons, check to see if the page is
loaded as an "application/xhtml+xml" page (you can see this in Firefox
by navigating to Tools->Page Info).  If it is not, be sure that SSI
are enabled (see above for enabling authconfig in Apache).

CITATION:

B. C. Russell, A. Torralba, K. P. Murphy, W. T. Freeman, LabelMe: a
database and web-based tool for image annotation. MIT AI Lab Memo
AIM-2005-025, September, 2005.

(c) 2005, MIT Computer Science and Artificial Intelligence Laboratory
With contributions from Samuel Davies, Erica Cooper, Juventino Mejia
