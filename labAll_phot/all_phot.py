#!/scisoft/bin/python

#!/scisoft//i386/bin/python
#/usr/bin/python/


##########
##########
# You will be changing all the parameters in here that you would have changed in easy_phot_params.py.
# I am essentially for looping easy_phot and so I feed the param file update variable names.
# This only uses iraf and no astropy so it can run on UW astro computers.
# One can use any number of star to measure you will just have to skip lines when you pull
# out columns of HJD, magX, and merrX.




import numpy as np # for vectorized arrays
import os,sys,subprocess

# Import IRAF and packages to use
from pyraf import iraf,pyrafglobals
iraf.imutil() # For hselect to grab from fits headers

import easy_phot as ep # for running methods in easy_phot.py specifically "execute()"


############
############ Parameter Lists (You only need to change this part!)

# WARNING: when you make your lists double check them to see that you have the same number of
# parameters that goes for each group of images. For example if you have 5 different days worth
# of images, lc_out_list_file should have 5 subsequent names for the 5 different days. Do not
# give names that are the same because files will get overwritten likely. I attempt to put into
# place error checking so that the program will exit if list sizes don't match up as they should.

final_file_name = "phot_final.txt" # name your final output file


lc_out_list_file = "lc_out_list_file.txt"
coords_list_file = "coords_list_file.txt"

image_dir = "/home/tristan/Astro481/Project2/test/" # specify directory with all the images in it
rootstr_list_file = "rootstr_list_file.txt"
endstr_list_file = "fits" # specify one end string for all files or one for each group of files


# Read the following carefully. In general each parameter takes a list that has your different parameter
# for each grouping of images.  The hiclip, lowclip, sigma values, however, can be set for either
# a single number across the board or for each individual group; give a number for all the images or a
# list with a value assigned to each group of images.
fwhmpsf_list_file = "fwhmpsf_list_file.txt"  # one for each group of images
sigma_list_file = 20.0 # Standard deviation of background in counts; one for all the images or of each group of images
hiclip_list_file = 30.0       # High sky annulus clipping, percent; one for all images or for each group of images
lowclip_list_file = 10.0     # Low sky annulus clipping, percent; one for all images or for each group of images
egain = 2.98      # CCD electron gain keyword  # specify CCD gain here
ccdread = 56.69     # CCD read noise keyword   # specify CCD readnoise here
amass = "AIRMASS"    # Airmass keyword
#obstime = "TIME-OBS" # Observation time keyword # just ignore this
obstime = "UT" # Observation time keyword
exp = "EXPOSURE"     # Exposure time keyword, seconds
annulus_list_file = "annulus_list_file.txt"   # annulus inner radius #specify annulus for each group of images
dannulus_list_file = "dannulus_list_file.txt"	# annulus width   # specify dannulus fore each group of images
skyvalue_list_file = "skyvalue_list_file.txt"  # background level  # specify background level for each group of images
header_items = ["AIRMASS"] # fill out this list with strings of keywords for items to grab from the image header
                                  # look in headers for keywords
############
############

# commented code; look over this if you are curious but you won't have to change anything here.
def main():

    # Make lists of each for Everything
    lc_out_list = np.genfromtxt(lc_out_list_file, usecols=[0], dtype='str')

    coords_list = np.genfromtxt(coords_list_file, usecols=[0], dtype='str')

    rootstr_list = np.genfromtxt(rootstr_list_file, usecols=[0], dtype='str')

    isOneRootStr = False
    if(rootstr_list.size == 1):
        isOneRootStr = True

    # check to see if endstr is static
    endstr_list = []
    if(os.path.isfile(endstr_list_file)): # look for file
        endstr_list = np.genfromtxt(endstr_list_file, usecols=[0], dtype='str') # if multiple ending string
        if isOneRootStr is not True:
            checkSameSize(rootstr_list, endstr_list, "root string", "end string") # check list size
    else:
        ep.endstr = endstr_list_file  # if only one ending str

    fwhmpsf_list = np.loadtxt(fwhmpsf_list_file, usecols=[0])

    annulus_list = np.loadtxt(annulus_list_file, usecols=[0])

    dannulus_list = np.loadtxt(dannulus_list_file, usecols=[0])

    skyvalue_list = np.loadtxt(skyvalue_list_file, usecols=[0])

    sigma_list = []
    if(isinstance(sigma_list_file, float) or isinstance(sigma_list_file, int)):
        ep.sigma = 1.0 * sigma_list_file
    else:
        sigma_list = np.loadtxt(sigma_list_file, usecols=[0])
        if isOneRootStr is not True:
            checkSameSize(rootstr_list, sigma_list, "root string", "sigma_list") # check list size

    hiclip_list = []
    if(isinstance(hiclip_list_file, float) or isinstance(hiclip_list_file, int)):
        ep.hiclip = 1.0 * hiclip_list_file
    else:
        hiclip_list = np.loadtxt(hiclip_list_file, usecols=[0])
        if isOneRootStr is not True:
            checkSameSize(rootstr_list, hiclip_list, "root string", "hiclip") # check list size

    lowclip_list = []
    if(isinstance(lowclip_list_file, float) or isinstance(lowclip_list_file, int)):
        ep.lowclip = 1.0 * lowclip_list_file
    else:
        lowclip_list = np.loadtxt(lowclip_list_file, usecols=[0])
        if isOneRootStr is not True:
            checkSameSize(rootstr_list, lowclip_list, "root string", "lowclip") # check list size


    # Set the absolute static parameters like egain and ccdread for easy_phot_params.py
    ep.image_dir = image_dir
    ep.egain = egain * 1.0
    ep.ccdread = ccdread * 1.0
    ep.amass = amass
    ep.obstime = obstime
    ep.exp = exp


    #### Throw some errors that check list size
    if isOneRootStr is not True:
        checkSameSize(rootstr_list, lc_out_list, "root string", "lc_out")
        checkSameSize(rootstr_list, coords_list, "root string", "coordinate")
        checkSameSize(rootstr_list, fwhmpsf_list, "root string", "fwhmpsf")
        checkSameSize(rootstr_list, annulus_list, "root string", "annulus")
        checkSameSize(rootstr_list, dannulus_list, "root string", "dannulus")
        checkSameSize(rootstr_list, skyvalue_list, "root string", "skyvalue")

    ### Check for indef in coordinate files
    coordFiles = np.genfromtxt(coords_list_file, usecols=[0], dtype='str')
    noINDEF = []
    if isOneRootStr is not True:
        for k in range(coordFiles.size):
            noINDEF.append(checkIndef(coordFiles[k]))
    else:
        noINDEF.append(checkIndef(coordFiles))

    if False in noINDEF:
        print
        print "Exiting from program..."
        sys.exit(1)



    final = open(final_file_name, 'w')




    # For loop that feeds easy_phot update parameters for a run on certain images
    numOfExecutes = 0
    if isOneRootStr is not True:
        numOfExecutes = rootstr_list.size
    else:
        numOfExecutes = 1

    #if isOneRootStr is not True:
    for i in range(numOfExecutes):

        if isOneRootStr is not True:
            # Update parameters for easy_phot_params
            ep.lc_out = lc_out_list[i]
            ep.coofnamein = coords_list[i]
            ep.rootstr = rootstr_list[i]
            ep.fwhmpsf = fwhmpsf_list[i]
            ep.annulus = annulus_list[i]
            ep.dannulus = dannulus_list[i]
            ep.skyvalue = skyvalue_list[i]

            # Those parameters that may be a list or not.
            if(os.path.isfile(endstr_list_file)):
                ep.endstr = endstr_list[i]

            if(isinstance(sigma_list_file, str)):
                ep.sigma = sigma_list[i]

            if(isinstance(hiclip_list_file, str)):
                ep.hiclip = hiclip_list[i]

            if(isinstance(lowclip_list_file, str)):
                ep.lowclip = lowclip_list[i]
        else:
            # Update parameters for easy_phot_params
            ep.lc_out = lc_out_list
            ep.coofnamein = coords_list
            ep.rootstr = rootstr_list
            ep.fwhmpsf = fwhmpsf_list
            ep.annulus = annulus_list
            ep.dannulus = dannulus_list
            ep.skyvalue = skyvalue_list

            if(isinstance(sigma_list_file, str)):
                ep.sigma = sigma_list
            if(isinstance(hiclip_list_file, str)):
                ep.hiclip = hiclip_list
            if(isinstance(lowclip_list_file, str)):
                ep.lowclip = lowclip_list
            if(isinstance(sigma_list_file, str)):
                ep.sigma = sigma_list


        # This runs easy_phot.py
        standard_output = sys.stdout # pass stdout to a variable rather than console
        f = open("easy_out.txt", 'w') # make a temporary file
        sys.stdout = f # prepares to dump stdout into file

        ep.execute() # execute easy_phot.py

        sys.stdout = standard_output # gives back stdout to console
        f.close()

        # Get the file names of this easy_phot.py instance
        f = open("easy_out.txt", 'r')

        fileList=[] # list for storing fits file names

        # goes through every line in the easy_phot.py console output file and isolates the fits file names
        # for storage.
        for line in f:
            if(line.startswith("/")):
                file = line.split("/")
                file = file[len(file) - 1]
                file = file.split("\n")
                file = file[0]
                fileList.append(file)
            else:
                continue

        f.close()



        # Get the JD from file header
        HJD = []
        for fileName in fileList:
            for item in header_items:
                header_HJD = iraf.hselect(images=fileName, fields=item , expr="yes", missing="INDEF", Stdout=1)
                HJD.append(header_HJD[0])

        HJD = np.asarray(HJD)

        mag = []
        merr = []

        # Get the number of stars from coordinate_list made by easy_phot.py
        numMeasurements = np.loadtxt("coords_list.txt", usecols=[0]).size

        # Grab mag values and mag error values
        for j in range(1, 2 * numMeasurements + 1):
            if(j % 2 == 1):
                if isOneRootStr is not True:
                    temp_mag = np.genfromtxt(lc_out_list[i], usecols=[j], dtype='str')
                else:
                    temp_mag = np.genfromtxt(str(lc_out_list), usecols=[j], dtype='str')
                mag.append(temp_mag)
            else:
                if isOneRootStr is not True:
                    temp_merr = np.genfromtxt(lc_out_list[i], usecols=[j], dtype='str')
                else:
                    temp_merr = np.genfromtxt(str(lc_out_list), usecols=[j], dtype='str')
                merr.append(temp_merr)


        # Write to everything to one file

        # Write a header line
        if(i == 0): # runs only once in the first loop
            num_header_items = len(header_items)
            final.write("name")
            for j in range(num_header_items):
                final.write(",%s"%header_items[j])
            for k in range(1, numMeasurements + 1):
                final.write(",Star%d"%k)
                final.write(",Star%d_err"%k)
            final.write("\n")

        for j in range(len(fileList)):
            final.write("%s,"%fileList[j])
            for num_item in range(num_header_items):
                final.write("%s,"%HJD[num_header_items * j + num_item])

            final.write("%s,"%mag[0][j])
            final.write("%s"%merr[0][j])
            for k in range(1, numMeasurements):
                final.write(",%s"%mag[k][j])
                final.write(",%s"%merr[k][j])
            final.write("\n")

        # Remove temporary files
        os.remove("easy_out.txt")

    # exit for loop and put finishing touches on.
    final.close()



def checkSameSize(mainList, checkAgainst, mainListName, listName):
    if(len(checkAgainst) != len(mainList)):
        print "Error the %s list did not match the size of the %s list...exiting program"%(mainListName, listName)
        sys.exit(1)

def checkIndef(fileName):
    indefCheck = open(fileName, 'r')
    noINDEF = True
    for line in indefCheck:
        line = map(str, line.split())
        if "INDEF" in line:
            print
            print "There are INDEFs present in the file %s...please correct..."%fileName
            noINDEF = False
            break
    return noINDEF


main() # run the main program
