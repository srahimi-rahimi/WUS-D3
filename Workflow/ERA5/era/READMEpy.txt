#This short readme shows the order in which I
#run the python scripts

#Between these steps, there are files
#that must be created, for instance,
#namelists and such.

#Run misc.py to check the number of files 
#are the same

DONT FORGET ABOUT move_leap.py!!!!!

1.  check_metem.py
2.  name.py
3.  mkdir.py
4.  qsub_real.py
5.  max_dom4to1.py
6.  qsub_wrf45km.py (then move_spin.py and move_leap.py)
7.  max_dom1to2.py
8.  qsub_ndown45to9km.py
9.  name_run9km.py
10. qsub_wrf9km.py  (then move_spin.py and move_leap.py)
11. name_ndown9to3km.py
12. qsub_ndown9to3km.py
13. name_run3km.py
14. qsub_wrf3km.py (move_spin.py and move_leap.py)
15. Repeat 11-14 for d04
