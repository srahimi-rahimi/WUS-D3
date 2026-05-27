#Created by S. Rahimi on 1 Jan. 2020
#to submit real.sh from 2015-2100

import subprocess as sb
import os
import shutil

#WRF direcotries located in:
dir = "/glade/scratch/srahimi/runERA5/WRF/test/"

cur_dir = "/glade/work/srahimi/labfees/wrf/era/"

year1, year2 = 2020, 2021

for iyear in range(year1,year2):

 os.chdir(cur_dir)

 #Create directory <iyear>
 dir_new = dir+"ERA_"+str(iyear)
 print (dir_new)

 #Navigate to new directory
 os.chdir(dir_new)

 os.system("qsub ndown_9to3km_d04.sh")

 #Return to the parent codes directory
 os.chdir(cur_dir)
