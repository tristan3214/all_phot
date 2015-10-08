#!/scisoft/bin/python

#!/scisoft//i386/bin/python
#/usr/bin/python/

#just like in IRAF, packages must be loaded

import sys, os, shutil, signal, math, types
from numpy import *
import pdb # python debugger

#numpy is the NUMber PYthon package that can do array math

from pyraf import iraf #,irafglobals
iraf.images()
iraf.imutil()
iraf.noao()
iraf.digiphot()
iraf.ptools()
iraf.daophot()

from easy_phot_params import *
#this loads all of the variables defined in easy_phot_params

def stringtohours(str):
    hrs,mins,secs = map(float,str.split(":"))
    return hrs+mins/60. + secs/3600.

def execute():

    #here we define the coords variable as a list
    coords=[]

    #indenting matters in python. Everything
    #indented under the for loop is inside the loop
    #pdb.set_trace() # break point for python debugger
    for line in open(coofnamein):
        if (line.startswith("#") or line.startswith("z1")):
            continue
        #this skips the lines that start with a #
        line=map(float,line.split())
        #this takes the line and splits it into a list of floats
        if len(line) != 4:
            continue
        #skips the lines that don't have 4 floats
        coords.append((line[0],line[1]))
        #adds the most recent coords (the 0th and 1st elements
        # to the list of coordinates

        #print coords

    coofnameout1=open(coofnameout, "w")

    for ci in coords:
        coofnameout1.write("%.4g\t%.4g\n" % ci)
        #the strange syntax is the formatting for the
        #output. It prints each coordinate with 4 decimal places
        # a tab in between, and then a new line at the end
    coofnameout1.close()
    #sys.exit(1)

    l=os.listdir(image_dir)
    l=[li for li in l if li.endswith(endstr)]
    l=[li for li in l if li.startswith(rootstr)]
    l =[image_dir + li for li in l]
    #this list takes all the files in the directory,
    #then only keeps those with the correct beginning and ending

    #l = l[:10]
    #this line can tell the code to only run on the first 10 images
    #useful for debugging

    lc_out1 = open(lc_out,"w")
    for li in l:
        print li
        #print coofnameout
        #print phot_out
        iraf.phot(li,coofnameout, phot_out, plotfile="", datapars="", centerpars="", fitskypars="", photpars="",interactive="no", radplots="no", icommands="", gcommands="", verify="no", weighting="constant", calgorithm="centroid", obstime=obstime, annulus=annulus,dannulus=dannulus,skyvalue=skyvalue,fwhmpsf=fwhmpsf,sigma=sigma)
        #this actually does the photometry
        #note all of the parameters that must be defined

        standard_output = sys.stdout
        #saves the current output -ie to the screen
        txdumpfile = open(txdumpout, 'w')
        sys.stdout = txdumpfile
        #directs the output to the txdumpfile

        iraf.txdump(phot_out, "otime,mag,merr", "yes", headers="no", parameters="no")
        #does the txdump - might you want to output other information?

        sys.stdout = standard_output # restores the stdout
        txdumpfile.close() # close the file
        os.remove(phot_out)
        #deletes the file

        phots  =[]

        for line in open(txdumpout):
            #line=map(string,line.split())
            line=str.split(line)
            phots.append((line[1],line[2]))
            #print phots

        #print line[0]

        #lc_out1.write(line[0] + "\t")
        #print stringtohours(line[0])
        lc_out1.write( "%10.7f \t" % (stringtohours(line[0])))


        for photsi in phots:
            lc_out1.write(photsi[0] + "\t")
            lc_out1.write(photsi[1] + "\t")
        lc_out1.write("\n")

        os.remove(txdumpout)

#r=execute()
