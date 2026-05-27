#! /bin/csh -f
#!/bin/bash
#PBS -N 1516_d1
#PBS -A WYOM0125
#PBS -q economy
#PBS -l walltime=06:03:00
#PBS -l select=4:ncpus=4:mpiprocs=4
#PBS -o log.oe

#mpiexec_mpt dplace -s 1 ./real.exe

#cp wrfinput_d04 wrfndi_d02
#cp wrflow* ./
#ln -sf d02/wrfout* ./
#mpiexec_mpt dplace -s 1 ./ndown.exe
#rm wrfout*
#cp wrfbdy_d02 wrfbdy_d01
#cp wrfinput_d02 wrfinput_d01
#cp d01/wrflowinp_d04 wrflowinp_d01

mpiexec_mpt dplace -s 1 ./wrf.exe
cp auxhist_d01_*-08-31_1[9]:00:00 d04
cp auxhist_d01_*-08-31_2[0-3]:00:00 d04

