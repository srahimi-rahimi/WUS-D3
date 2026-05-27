#Created by S. Rahimi on 31 Dec. 2019
#to submit real.sh from 2015-2100

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

 os.system("qsub real.sh")

 #Return to the parent codes directory
 os.chdir(cur_dir)
