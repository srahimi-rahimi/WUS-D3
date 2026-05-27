#!/bin/bash -l
#SBATCH -J re
#SBATCH -n 1
#SBATCH --ntasks-per-node=1
#SBATCH -t 6:00:00
#SBATCH -A WYOM0125
#SBATCH --mem 50G
#SBATCH -p dav
#SBATCH -C casper
#SBATCH -e slurmhtar.err.%J
#SBATCH -o slurmhtar.out.%J

#For Python scripts only
deactivate
source /glade/work/srahimi/casper/20190723/bin/activate

python test.py
