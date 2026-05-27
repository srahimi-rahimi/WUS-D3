#!/bin/bash
#PBS -N ndown
#PBS -A WYOM0125
#PBS -q economy
#PBS -l walltime=12:00:00
#PBS -l select=1:ncpus=36:mpiprocs=36
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

cp -rp d01/wrfinput_d04 wrfndi_d02
ln -sf d02/spin_up/wrfout* ./
ln -sf d02/ly/wrfout* ./
ln -sf d02/wrfout* ./
mpiexec_mpt dplace -s 1 ./ndown.exe
rm wrfout*
cp -rp wrfbdy_d02 wrfbdy_d01
cp -rp d01/wrfinput_d04 wrfinput_d01
cp -rp wrflowinp_d04 wrflowinp_d01
