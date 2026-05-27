#! /bin/csh -f
#!/bin/bash
#PBS -N metgrid
#PBS -A WYOM0125
#PBS -q economy
#PBS -l walltime=12:00:00
#PBS -l select=1:ncpus=36:mpiprocs=36
#PBS -o log.oe

export TMPDIR=/glade/scratch/$USER/temp
mkdir -p $TMPDIR

mpiexec_mpt ./metgrid.exe > &! metgrid.out
