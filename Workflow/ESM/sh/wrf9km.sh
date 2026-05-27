#!/bin/bash
#PBS -N 1516_d2
#PBS -A WYOM0136
#PBS -q premium
#PBS -l walltime=12:00:00
#PBS -l select=6:ncpus=36:mpiprocs=36
#PBS -o log.oe

export WRF_CHEM=0
export EM_CORE=1
export WRF_EM_CORE=1
export WRFIO_NCD_LARGE_FILE_SUPPORT=1
export WRF_KPP=0
export YACC="/usr/bin/yacc -d"
export FLEX_LIB_DIR="/usr/lib64/"

module load mpt/2.22
module load intel/17.0.1
module load ncarenv/1.2
module load ncarcompilers/0.4.1
module load netcdf/4.5.0

mpiexec_mpt dplace -s 1 ./wrf.exe

mv wrfout* d02
mv auxhist* d02
