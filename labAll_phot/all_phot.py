#!/scisoft/bin/python

#!/scisoft//i386/bin/python
#/usr/bin/python/

##########
##########
# I am essentially for looping easy_phot.
# This only uses iraf and no astropy so it can run on UW astro computers.



import numpy as np # for vectorized arrays
import os,sys

# Import IRAF and packages to use
from pyraf import iraf
iraf.imutil() # For hselect to grab from fits headers

import easy_phot as ep # for running methods in easy_phot.py specifically "execute()"

parameterFile = sys.argv[-1]
param_file = open(parameterFile, 'r')
param_lines = [line.rstrip('\n') for line in param_file]
param_file.close()


if(len(param_lines) is not 16):
    print "Error...You have %d unique lines in the parameter file there should be 16."%len(param_lines)
    print "Exiting program..."
    sys.exit(1)



############
############ Global Parameters (You only make a parameter file!!)

amass = "AIRMASS"    # Airmass keyword
#obstime = "TIME-OBS" # Observation time keyword # just ignore this
obstime = "UT" # Observation time keyword
exp = "EXPOSURE"     # Exposure time keyword, seconds


# phase out the old way slowly
final_file_name = param_lines[0]
image_dir = param_lines[3]
header_items = np.asarray(param_lines[15].split(" "))
egain = float(param_lines[10])
ccdread = float(param_lines[11])



############
############

# commented code; look over this if you are curious but you won't have to change anything here.
def main():

    # Make lists of each for Everything
    lc_out_list = np.asarray(param_lines[1].split(" "))

    coords_list = np.asarray(param_lines[2].split(" "))

    rootstr_list = np.asarray(param_lines[4].split(" "))

    isOneRootStr = False
    if(rootstr_list.size == 1):
        isOneRootStr = True

    # check to see if endstr is static
    endstr_list = np.asarray(param_lines[5].split(" "))
    if(endstr_list.size == 1):
        ep.endstr = endstr_list[0]  # if only one ending str
    else:
        checkSameSize(rootstr_list, endstr_list, "root string", "end string") # check list size

    fwhmpsf_list = np.asarray(map(float, param_lines[6].split(" ")))

    annulus_list = np.asarray(map(float, param_lines[12].split(" ")))

    dannulus_list = np.asarray(map(float, param_lines[13].split(" ")))

    skyvalue_list = np.asarray(map(float, param_lines[14].split(" ")))

    sigma_list = np.asarray(map(float, param_lines[7].split(" ")))
    if(sigma_list.size == 1):
        ep.sigma = 1.0 * sigma_list[0]
    else:
        checkSameSize(rootstr_list, sigma_list, "root string", "sigma_list") # check list size

    hiclip_list = np.asarray(map(float, param_lines[8].split(" ")))
    if(hiclip_list.size == 1):
        ep.hiclip = 1.0 * hiclip_list[0]
    else:
        checkSameSize(rootstr_list, hiclip_list, "root string", "hiclip") # check list size

    lowclip_list = np.asarray(map(float, param_lines[9].split(" ")))
    if(lowclip_list.size == 1):
        ep.lowclip = 1.0 * lowclip_list[0]
    else:
        checkSameSize(rootstr_list, lowclip_list, "root string", "lowclip") # check list size


    # Set the absolute static parameters like egain and ccdread for easy_phot_params.py
    ep.image_dir = image_dir
    ep.egain = egain * 1.0
    ep.ccdread = ccdread * 1.0
    ep.amass = amass
    ep.obstime = obstime
    ep.exp = exp


    #### Throw some errors that check list size
    checkSameSize(rootstr_list, lc_out_list, "root string", "lc_out")
    checkSameSize(rootstr_list, coords_list, "root string", "coordinate")
    checkSameSize(rootstr_list, fwhmpsf_list, "root string", "fwhmpsf")
    checkSameSize(rootstr_list, annulus_list, "root string", "annulus")
    checkSameSize(rootstr_list, dannulus_list, "root string", "dannulus")
    checkSameSize(rootstr_list, skyvalue_list, "root string", "skyvalue")

    ### Check for indef in coordinate files
    #coordFiles = np.genfromtxt(coords_list_file, usecols=[0], dtype='str')
    noINDEF = []
    if isOneRootStr is not True:
        for k in range(coords_list.size):
            noINDEF.append(checkIndef(coords_list[k]))
    else:
        noINDEF.append(checkIndef(coords_list))

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

        # Update parameters for easy_phot_params
        ep.lc_out = lc_out_list[i]
        ep.coofnamein = coords_list[i]
        ep.rootstr = rootstr_list[i]
        ep.fwhmpsf = fwhmpsf_list[i]
        ep.annulus = annulus_list[i]
        ep.dannulus = dannulus_list[i]
        ep.skyvalue = skyvalue_list[i]

        # Those parameters that may be a list or not.
        if(endstr_list.size > 1):
            ep.endstr = endstr_list[i]

        if(sigma_list.size > 1):
            ep.sigma = sigma_list[i]

        if(hiclip_list.size > 1):
            ep.hiclip = hiclip_list[i]

        if(lowclip_list.size > 1):
            ep.lowclip = lowclip_list[i]


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
        header_data = []
        for fileName in fileList:
            for item in header_items:
                data = iraf.hselect(images=fileName, fields=item , expr="yes", missing="INDEF", Stdout=1)
                header_data.append(data[0])

        header_data = np.asarray(header_data)

        mag = []
        merr = []

        # Get the number of stars from coordinate_list made by easy_phot.py
        numMeasurements = np.loadtxt("coords_list.txt", usecols=[0]).size

        # Grab mag values and mag error values
        for j in range(1, 2 * numMeasurements + 1):
            if(j % 2 == 1):
                temp_mag = np.genfromtxt(lc_out_list[i], usecols=[j], dtype='str')
                mag.append(temp_mag)
            else:
                temp_merr = np.genfromtxt(lc_out_list[i], usecols=[j], dtype='str')
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
                final.write("%s,"%header_data[num_header_items * j + num_item])

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
    for j in lc_out_list:
        os.remove(j)

    print
    print "Program exited correctly...look for %s as your output file."%final_file_name

    print
    print "If the outputed file is missing lines make sure your rootstr and endstr arguements are correct."



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
