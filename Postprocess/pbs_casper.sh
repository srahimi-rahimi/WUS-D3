#!/bin/bash
#PBS -N xxx
#PBS -A WYOM0227
#PBS -q casper
#PBS -l walltime=08:00:00
#PBS -l select=1:ncpus=1:mpiprocs=1:mem=32GB
#PBS -o log.oe

export TMPDIR=/glade/derecho/scratch/leihuang/temp
mkdir -p $TMPDIR

module load conda
conda activate my-env-npl

module load peak-memusage

#Run the script here
