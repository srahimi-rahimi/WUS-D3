#Created by S. Rahimi on 26 Jan. 2020
#to create yearly directories in /test
#Also copies the namelists created by
#name.py into said directories
#copies *sh files into said directories
#links *exe files into said directories
#links met_em files to directories

#ERA5

import subprocess as sb
import os
import shutil

#WRF direcotries located in:
dir = "/glade/derecho/scratch/srahimi/wus/era5/WRF/test/"

#WPS directory located in: (location of COMPLETED met_em files)
metgrid_dir = "/glade/derecho/scratch/srahimi/wus/era5/WPS/"

cur_dir = "/glade/work/srahimi/labfees/wrf/era/"

#Namelist directory
name_dir = cur_dir+"/namelist.input_real_files_ERA/"

year1, year2 = 2023, 2025

for iyear in range(year1,year2):

 os.chdir(cur_dir)

 #Create directory <iyear>
 dir_new = dir+"ERA_"+str(iyear)
 print (dir_new)
 #sb.call(['mkdir',dir_new])

 #Copy *.sh files to new directory
 directive = "cp sh/*sh %s" %(dir_new) 
 os.system(directive)

 #Navigate to new directory
 os.chdir(dir_new)

 #Run link.sh
 #sb.call(['./link.sh'],shell=True)

 #Create d01, d02, d03, and d04 directories
 #sb.call(['mkdir d01'],shell=True)
 #sb.call(['mkdir d02'],shell=True)
 #sb.call(['mkdir d03'],shell=True)
 #sb.call(['mkdir d04'],shell=True)

 #Link met_em files to directory
 #for iiyear in range(iyear,iyear+2):
 # directive = "ln -sf %smet_em.d0*.%s* ./" %(metgrid_dir,iiyear)
 # os.system(directive)

 #Copy the namelist.input to the directory
 directive = "cp %snamelist.input_real_%s_ERA ./namelist.input_real" %(name_dir,iyear)
 os.system(directive)
 os.system("cp namelist.input_real namelist.input")

 #Return to the parent codes directory
 os.chdir(cur_dir)
