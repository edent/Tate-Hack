Tate-Hack
=========

A collection of faces for #hackthespace.

This script uses Python to download all the images from https://github.com/tategallery/collection/blob/master/artist_data.csv

It runs the image through OpenCV's face recognition.

If a face is detected, it crops the face and saves it as a separate image.  This will detect multiple faces per image.
