#Created by S. Rahimi on 31 Mar. 2020
#to move spin-up wrfout/auxhit files
#to <year>/<domain>/spin_up

import subprocess as sb
import os
import shutil

#WRF direcotries located in:
dir = "/glade/derecho/scratch/srahimi/wus/era5/WRF/test/"

domain = "d03"
year1, year2 = 2023, 2025

for iyear in range(year1,year2):

 dir_new = dir+"ERA_"+str(iyear)

 dir_d = dir_new+"/"+domain

 directive = "mkdir %s/spin_up" %(dir_d)
 os.system(directive)

 #wrfout
 directive = "ls -l %s/wrfout_d01* | wc -l" %(dir_d)
 os.system(directive)
 directive = "mv %s/wrfout_d01_%s-08* %s/spin_up" %(dir_d,iyear,dir_d)
 os.system(directive)
 #directive = "mv %s/wrfout_d01_%s-09* %s/spin_up" %(dir_d,iyear+1,dir_d)
 #os.system(directive)
 directive = "ls -l %s/wrfout_d01* | wc -l" %(dir_d)
 os.system(directive)

 #auxhist
 directive = "ls -l %s/auxhist_d01* | wc -l" %(dir_d)
 os.system(directive)
 directive = "mv %s/auxhist_d01_%s-08* %s/spin_up" %(dir_d,iyear,dir_d)
 os.system(directive)
 directive = "mv %s/auxhist_d01_%s-09* %s/spin_up" %(dir_d,iyear+1,dir_d)
 #os.system(directive)
 directive = "ls -l %s/auxhist_d01* | wc -l" %(dir_d)
 os.system(directive)

 print ("||||||---", iyear, "---||||||")
