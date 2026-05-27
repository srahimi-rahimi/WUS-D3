#Created by S. Rahimi on 1 Jan. 2020
#to change max_dom in namelist.input file
#before running ndown.exe

import subprocess as sb
import os
import shutil

domain = "d02"	#We are ndowning to.....

#WRF direcotries located in:
dir = "/glade/scratch/srahimi/taiesm1/WRF/test/"

#WPS directory located in: (location of COMPLETED met_em files)
metgrid_dir = "/glade/scratch/srahimi/taiesm1/met_em_files/"

cur_dir = "/glade/work/srahimi/labfees/wrf/taiesm/"

year1, year2 = 1980,2100

for iyear in range(year1,year2,1):

 os.chdir(cur_dir)

 #Create directory <iyear>
 dir_new = dir+"TAIESM_"+str(iyear)

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

 max_dom = " max_dom                          = 2\n"

 #Copy parameters to new namelist
 for ii in lines_old:
  if not ii.startswith(" max_dom"):
   fnew.writelines(ii)
  if ii.startswith(" max_dom"):
   fnew.writelines(max_dom)

 fnew.close()

 if domain == "d02":
  os.system("cp namelist.input namelist.input_ndown45to9km")
 if domain == "d03":
  os.system("cp namelist.input namelist.input_ndown9to3km_CA") 
 if domain == "d04":
  os.system("cp namelist.input namelist.input_ndown9to3km_WY")

 #Return to the parent codes directory
 os.chdir(cur_dir)
