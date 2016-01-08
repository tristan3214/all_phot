# all_phot
This is a wrapper script to a program written by someone, who's name eludes me, at the University of Washington that performs aperture photometry on a set of images.


I have overhauled all_phot so that one no longer needs to have a plethora of text files defining
the different attributes of each needed parameter.

This will detail on how on single "parameter" file is used to specify all the needed parameters.
There will also be example scenarios of parameter file given in the folder examples.

If you want to use this code on a UW astrolab computer you will need to start a Ureka terminal.

# How To Use
The parameter file consists of 16 lines that define all there is needed to run all_phot properly.
Following will be a line by line description of each parameter, and keep in mind that multiple arguments per line MUST be delimeted by white space. Read the debug section for solutions to common problems.

line1: This is were you give the name of master output file, e.g. final_phot.dat

line2: easy_phot creates data files for each batch of images that need to be named so just give some arbitrary name, e.g. data1.dat data2.dat ...

line3: For each batch of images you made a coordinate file like you would for easy_phot.  This file consists of raw imexam data of each star you want to measure.  Give a name for each coordinate file that represents each new batch of images.

line4: This is where you specify your image directory where ALL your photos are held.

line5: Specify the root string name for each batch, e.g. if I have images rimage_0.fit where 0 changes depending on the image number the root string is "rimage".

line6: Here is where one specifies the end string name.  One can specify one name for all the images or many for each batch of images.

line7: Need a general fwhmpsf value for each batch of images.  For example if I have 6 stars each with an fwhmpsf, found using imexam, then I would take the average of all of them and use that value.

line8: Need a sigma value of the background skyvalue.  Can specify one for each batch or one for all.

line9: Specify a hiclip value for either all the images or for each batch of images.

line10: Specify a lowclip value for either all the images or for each batch of images.

line11: Give a value of the CCD gain in units of electrons per ADU.

line12: Give a value of CCD read noise in units of ADUs.

line13: Give an annulus value for each batch of images.

line14: Give an dannulus value for each batch of images.

line15: Give a skyvalue of each batch of images in units of ADUs.

line16: Specify which keyword values you want to extract from the fits headers. (e.g. AIRMASS) The ordering here will appear as is in the all_phot output.

Once your parameter file is setup you run all_phot using the following command:

        python all_phot.py parameterFile.txt

#Common Problems
There are no major bugs to be seen, and the way the program is setup is so that they only have to edit one file.  This redirects any worry for the user from having to edit the .py files directly like in the past with easy_phot.py; that is a volatile task and can lead to user error.  As long as the user follows the directions and runs through the example for extra help they should be successful in correctly running the program.

# Automatic Error Checking Features
The program has some built in features to check for some common errors that I noticed users were getting during normal usage of easy_phot.py:
    1. There is a rudimentary system to check that the user has entered the correct amount of arguments in the parameter file based on the number of root strings present.  For example, if one gives two root strings then the program will check that there are two coordinate files names listed and so on.  If it doesn't successful pass this error checking the program will state which "list" is not matching up with the root string "list".

    2. When using imexam to make a raw coordinate list sometimes it will produce INDEFs in non-essential quantities that break easy_phot.py.  This program attempts to find any INDEFs in these coordinate files and will notify the user which ones have them and exit the program abnormally.

# Limitations
1. There is only one glaring limitation to the program.  That is the fact that this program is intended to look at images of the same field that may be across different days measuring the same number of stars.  This means that one can not take two completely different fields wanting to measure a different number of stars in each.  However, I suppose, one could still use this program on completely different fields as long as they measure the same amount of stars in each.

2. A subtle detail is that that during the root string list size checking it does not make sure there is either only one or as many values in the arguements that can have either one specification or many.  Those are paramter arguements like low clip and high clip.

#Future Work
1. Get the name of the person that originally wrote easy_phot and give them the proper credit since that is the back bone in the all_phot scrip.

2. Merge easy_phot into all_phot.

3. Try to make into an executable application similar to a .exe file on windows.
