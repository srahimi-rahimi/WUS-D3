#Created by S. Rahimi on 1 Jan. 2020
#to submit wrf45km.sh from 2015-2100

import subprocess as sb
import os
import shutil

#WRF direcotries located in:
dir = "/glade/scratch/srahimi/taiesm1/WRF/test/"

#WPS directory located in: (location of COMPLETED met_em files)
metgrid_dir = "/glade/scratch/srahimi/taiesm1/met_em_files/"

cur_dir = "/glade/work/srahimi/labfees/wrf/taiesm/"

year1, year2 = 1980, 2100

for iyear in range(year1,year2,1):

 if iyear == 1988:
  continue

 os.chdir(cur_dir)

 #Create directory <iyear>
 dir_new = dir+"TAIESM_"+str(iyear)

 print (dir_new)

 #Navigate to new directory
 os.chdir(dir_new)

 os.system("qsub wrf9km.sh")

 #Return to the parent codes directory
 os.chdir(cur_dir)
