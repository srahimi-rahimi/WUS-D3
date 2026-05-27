#!/bin/bash
#PBS -N ndown
#PBS -A WYOM0200
#PBS -q main
#PBS -l walltime=12:00:00
#PBS -l select=1:ncpus=36:mpiprocs=36
#PBS -o log.oe

export WRF_CHEM=0
export EM_CORE=1
export WRF_EM_CORE=1
export WRFIO_NCD_LARGE_FILE_SUPPORT=1
export WRF_KPP=0
export YACC="/glade/u/apps/gust/23.04/opt/bin/yacc -d"
export FLEX_LIB_DIR="/glade/u/apps/gust/23.04/opt/lib"

module --force purge
module load ncarenv/23.06
module load intel-classic/2023.0.0
module load hdf5/1.12.2
module load cray-mpich/8.1.25
module load ncview/2.1.8
module load craype/2.7.20
module load netcdf/4.9.2
module load ncarcompilers/1.0.0

cp -rp d01/wrfinput_d03 wrfndi_d02
ln -sf d02/spin_up/wrfout* ./
ln -sf d02/ly/wrfout* ./
ln -sf d02/wrfout* ./
mpiexec ./ndown.exe
rm wrfout*
cp -rp wrfbdy_d02 wrfbdy_d01
cp -rp wrfbdy_d02 d03/wrfbdy_d02_ndown
cp -rp d01/wrfinput_d03 wrfinput_d01
cp -rp d01/wrflowinp_d03 wrflowinp_d01
