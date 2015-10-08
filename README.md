# all_phot
This is a wrapper script to a program written by someone, who's name eludes me, at the University of Washington that performs aperture photometry on a set of images.

The changes are you can now specify, in the header_items variable, what you want to be pulled out of the image headers.  It can even take many arguements such as if you want HJD and AIRMASS you say header_item = ["HJD", "AIRMASS"].
