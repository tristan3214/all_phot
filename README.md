# all_phot
This is a wrapper script to a program written by someone, who's name eludes me, at the University of Washington that performs aperture photometry on a set of images.

Keep in mind there is a different version for the UW computers labs found in the folder labAll_phot.  For those using Ureka just use the version found in regAll_phot.  I personally have a broken profile when it comes to python and IRAF at the UW astro lab computers.  So once I get that fixed I can more readily know the differences between the two.  Also don't run this program while pyraf or iraf is active in your UW lab terminal.

I have overhauled all_phot so that one no longer needs to have a plethora of text files defining
the different attributes of each needed parameter.

This will detail on how on single "parameter" file is used to specify all the needed parameters.
There will also be example scenarios of parameter file given in the folder examples.

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
Coming soon!

#Future Work
1. Get the name of the person that originally wrote easy_phot and give them the proper credit since that is the back bone in the all_phot scrip.

2. Merge easy_phot into all_phot.

3. Try to make into an executable application similar to a .exe file on windows.
