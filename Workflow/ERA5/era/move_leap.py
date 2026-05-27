#Created by S. Rahimi on 8 May 2020
#to move spin-up wrfout/auxhit files
#to <year>/<domain>/ly

import subprocess as sb
import os
import shutil

#WRF direcotries located in:
dir = "/glade/scratch/srahimi/ucla/downscale/WRF/test/"

domain = "d04"
year1, year2 = 1951, 1980

for iyear in range(year1,year2,4):

 dir_new = dir+"ERA_"+str(iyear)

 dir_d = dir_new+"/"+domain

 print ("||||||---", iyear, "---||||||")

 directive = "mkdir %s/ly" %(dir_d)
 os.system(directive)

 #wrfout
 directive = "ls -l %s/wrfout_d01* | wc -l" %(dir_d)
 os.system(directive)
 directive = "mv %s/wrfout_d01_*02-29* %s/ly" %(dir_d,dir_d)
 os.system(directive)
 directive = "ls -l %s/wrfout_d01* | wc -l" %(dir_d)
 os.system(directive)

 #auxhist
 directive = "ls -l %s/auxhist_d01* | wc -l" %(dir_d)
 os.system(directive)
 directive = "mv %s/auxhist_d01_*02-29* %s/ly" %(dir_d,dir_d)
 os.system(directive)
 directive = "ls -l %s/auxhist_d01* | wc -l" %(dir_d)
 os.system(directive)

 directive = "ls -l %s/wrfout_d01* | wc -l" %(dir_d)
 os.system(directive)
 directive = "ls -l %s/auxhist_d01* | wc -l" %(dir_d)
 os.system(directive)

 print ("||||||---", iyear, "---||||||")
