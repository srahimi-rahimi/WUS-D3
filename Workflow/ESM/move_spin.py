#Created by S. Rahimi on 31 Mar. 2020
#to move spin-up wrfout/auxhit files
#to <year>/<domain>/spin_up

import subprocess as sb
import os
import shutil

domain = 'd03'

#WRF direcotries located in:
dir = "/glade/scratch/srahimi/taiesm1/WRF/test/"

#WPS directory located in: (location of COMPLETED met_em files)
metgrid_dir = "/glade/scratch/srahimi/taiesm1/met_em_files/"

cur_dir = "/glade/work/srahimi/labfees/wrf/taiesm/"

year1, year2 = 1980, 2100

for iyear in range(year1,year2,1):

 os.chdir(cur_dir)

 #Create directory <iyear>
 dir_new = dir+"TAIESM_"+str(iyear)

 dir_d = dir_new+"/"+domain

 directive = "mkdir %s/spin_up" %(dir_d)
 os.system(directive)

 #wrfout
 directive = "ls -l %s/wrfout_d01* | wc -l" %(dir_d)
 os.system(directive)
 directive = "mv %s/wrfout_d01_%s-08* %s/spin_up" %(dir_d,iyear,dir_d)
 os.system(directive)
 directive = "ls -l %s/wrfout_d01* | wc -l" %(dir_d)
 os.system(directive)

 #auxhist
 directive = "ls -l %s/auxhist_d01* | wc -l" %(dir_d)
 os.system(directive)
 directive = "mv %s/auxhist_d01_%s-08* %s/spin_up" %(dir_d,iyear,dir_d)
 os.system(directive)
 directive = "ls -l %s/auxhist_d01* | wc -l" %(dir_d)
 os.system(directive)

 print ("||||||---", iyear, "---||||||")
