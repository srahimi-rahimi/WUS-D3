#Created by S. Rahimi on 31 Dec. 2019
#to change max_dom in namelist.input file
#after running real.exe

import subprocess as sb
import os
import shutil

#WRF direcotries located in:
dir = "/glade/derecho/scratch/srahimi/wus/era5/WRF/test/"

cur_dir = "/glade/work/srahimi/labfees/wrf/era/"

year1, year2 = 2023, 2025

for iyear in range(year1,year2,1):

 os.chdir(cur_dir)

 #Create directory <iyear>
 dir_new = dir+"ERA_"+str(iyear)

 print (dir_new)

 #Navigate to new directory
 os.chdir(dir_new)

 #Change  max_dom of the namelist.input file

 #Read original namelist.input
 file = "namelist.input"
 fo = open(file,"r")
 lines_old = fo.readlines()

 #Write to new namelist.input file
 #but change max_dom
 fnew = open("namelist.input","w")

 max_dom = " max_dom                          = 1\n"

 #Copy parameters to new namelist
 for ii in lines_old:
  if not ii.startswith(" max_dom"):
   fnew.writelines(ii)
  if ii.startswith(" max_dom"):
   fnew.writelines(max_dom)

 fnew.close()

 #Copy namelist.input to namelist.input_run45km
 os.system("cp namelist.input namelist.input_run45km") 

 #Return to the parent codes directory
 os.chdir(cur_dir)
