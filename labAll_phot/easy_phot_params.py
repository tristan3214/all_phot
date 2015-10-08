import os,sys

#################### Predefined variables ####################################

# define temporary files

txdumpout = 'txdump_outputfile.tmp'



phot_out = "temp_photout.mag"


lc_out = "" # this is changed by all_phot

coofnamein="" # this is changed by all_phot
coofnameout="coords_list.txt"

### Will you need  to change some of the following?
image_dir = "" # changed by all_phot
rootstr = "" # changed by all_phot
endstr = "" # changed by all_phot

### LOOK! Are these parameters what you would have chosen? What are your criteria?
### How about those keywords?
### photometry parameters
### all of these are changed by all_phot and can be changed there rather
fwhmpsf=''
sigma = ''	# Standard deviation of background in counts
hiclip=''       # High sky annulus clipping, percent
lowclip=''      # Low sky annulus clipping, percent
egain=''    # CCD electron gain keyword
ccdread=''     # CCD read noise keyword
amass="AIRMASS"    # Airmass keyword
#obstime="TIME-OBS" # Observation time keyword
obstime="UT" # Observation time keyword
exp="EXPOSURE"     # Exposure time keyword, seconds
annulus=''   # annulus inner radius
dannulus=''	# annulus width
skyvalue=''

################### End of predefined #########################
