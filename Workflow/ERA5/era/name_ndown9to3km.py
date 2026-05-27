#Created by S. Rahimi on 26 Jan. 2020
#to update the namelist for each experiment

#Changes start_year and end_year in namelist.input

#CO2 & CH4 conc. set to ~default

import netCDF4
from netCDF4 import Dataset
import numpy as np
import subprocess
import os

#We are ndowning to....
domain = "d03"

dir = "/glade/derecho/scratch/srahimi/wus/era5/WRF/test/"

year0 = 2015
year1, year2 = 2023, 2025
#sector = 0, global; sector = 1, NH; sector = 2, SH
sector = 1

#For pre-2015
#MASTER DIRECTORY | where are your CESM2 historical files
dir_in = "/glade/work/srahimi/labfees/wrf/emissions_files/"
f_co2 = Dataset(dir_in+"mole-fraction-of-carbon-dioxide-in-air_input4MIPs_GHGConcentrations_CMIP_UoM-CMIP-1-2-0_gr1-GMNHSH_0000-2014.nc","r")
co2 = f_co2.variables["mole_fraction_of_carbon_dioxide_in_air"][:,sector]  #[ppmv]
f_ch4 = Dataset(dir_in+"mole-fraction-of-methane-in-air_input4MIPs_GHGConcentrations_CMIP_UoM-CMIP-1-2-0_gr1-GMNHSH_0000-2014.nc","r")
ch4 = f_ch4.variables["mole_fraction_of_methane_in_air"][:,sector]          #[ppbv]

#For 2015 onwards
f_co2 = Dataset(dir_in+"mole-fraction-of-carbon-dioxide-in-air_input4MIPs_GHGConcentrations_ScenarioMIP_UoM-AIM-ssp370-1-2-1_gr1-GMNHSH_2015-2500.nc","r")
co2_ssp = f_co2.variables["mole_fraction_of_carbon_dioxide_in_air"][:,sector]  #[ppmv]
f_ch4 = Dataset(dir_in+"mole-fraction-of-methane-in-air_input4MIPs_GHGConcentrations_ScenarioMIP_UoM-AIM-ssp370-1-2-1_gr1-GMNHSH_2015-2500.nc","r")
ch4_ssp = f_ch4.variables["mole_fraction_of_methane_in_air"][:,sector]          #[ppbv]

#Now create new namelists

for iyear in range(year1,year2):

 #Original file
 file_orig = "ndown9to3km_namelist.input"

 #Read original 2015 in preparation to
 #to copy updated contents to
 #namelist.input_real_<iyear>

 new_dir = "namelist.input_ndown9to3km_files/"
 new_file = "namelist.input_ndown9to3km_%s" %(iyear)
 fo = open(file_orig,"r")
 lines_old = fo.readlines()

 dir_new = dir+"ERA_"+str(iyear)

 fnew = open(new_dir+new_file,"w") 

 if (iyear+1) % 4 == 0:
  runday_str = " run_days                               = 397\n"

 if (iyear+1) % 4 != 0:
  runday_str = " run_days                                = 396\n"

 if iyear < 2015:
  co2_year = co2[iyear-1]
  ch4_year = ch4[iyear-1]

 if iyear >= 2015:
  co2_year = co2_ssp[iyear-year0]
  ch4_year = ch4_ssp[iyear-year0]

 co2_str = " co2_ppmv                            = %s\n" %(co2_year)
 ch4_str = " ch4_ppbv                            = %s\n" %(ch4_year)

 starty_str = " start_year                          = %s, %s, %s, %s\n" %(iyear,iyear,iyear,iyear)
 endy_str = " end_year                            = %s, %s, %s, %s\n" %(iyear+1,iyear+1,iyear+1,iyear+1)

 #Copy parameters to new namelist
 for ii in lines_old:
  if not ii.startswith(" co2_ppmv") and not ii.startswith(" ch4_ppbv") \
   and not ii.startswith(" start_year") and not ii.startswith(" end_year") \
   and not ii.startswith(" run_days"):
   fnew.writelines(ii)
  if ii.startswith(" run_days"):
   fnew.writelines(runday_str)
  if ii.startswith(" start_year"):
   fnew.writelines(starty_str)
  if ii.startswith(" end_year"):
   fnew.writelines(endy_str)
  if ii.startswith(" co2_ppmv"):
   fnew.writelines(co2_str)
  if ii.startswith(" ch4_ppbv"):
   fnew.writelines(ch4_str)

 fnew.close()

 #Copy namelist.input to test/* directory
 directive = "cp %s%s %s/namelist.input" %(new_dir,new_file,dir_new)
 os.system(directive)

 directive = "cp %s%s %s/namelist.input_ndown9to3km_%s" %(new_dir,new_file,dir_new,domain)
 os.system(directive)

 print (iyear, co2_year, ch4_year)
 print (dir_new)
 print (iyear)
