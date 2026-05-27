import os, glob

vars_1 = [ 'mrso', 'tsl', 'ivt', 'clivi', 'lwp', 'zg', 'hus', 'ta', 'ua', 'va', 'w_3d', 'cape', 'cin', 'lcl', 'lfc']
vars_2 = ['evspsbl', 'es', 'gh_sfc', 'hfls', 'ps', 'hfss', 'rsds', 'rlds', 'sw_sfc', 'lw_sfc', 'zmla', 'rlut',
          'snow', 'mrros', 'mrrob', 'ts', 'uv100', 'wspd100max', 'wspd100mean', 'prsn']
vars_3 = ['pr', 'prc', 'huss', 'tas', 'tasmax', 'tasmin', 'sfcWindmax', 'sfcWind', 'uv10', 'prec_max15min', 'prec_max30min', 'prec_max60min']
vars_all = vars_1 + vars_2 + vars_3
#vars_all = ['prec_max15min', 'prec_max30min', 'prec_max60min']
print(len(vars_1),len(vars_2),len(vars_3),len(vars_all))

# Command submission script template
pbs_orig = '/glade/work/leihuang/postprocess/pbs_casper.sh'

#For modifying the pbs.sh file
bogey = 'xxx'

# Set the input parameters
model_base = 'cesm2-le'
#model_base = 'era5'
variant = '1071'
domain = 'd02'
leap_flag = 0
bc_flag = 1
#in_dir  = f'/glade/derecho/scratch/leihuang/wus/cesm2_{variant}/WRF/test/'
in_dir  = f'/glade/derecho/scratch/weichenl/weichenl/wus_downscale/cesm2_{variant}/WRF/test/'
#in_dir = '/glade/campaign/uwyo/wyom0112/era5/'
#out_dir = f'/glade/derecho/scratch/leihuang/postprocess/cesm2-le/{variant}/{domain}/'
out_dir = f'/glade/derecho/scratch/leihuang/postprocess/cesm2_{variant}/{domain}/'
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

years = range(1981, 2100)
for year in years:
    model = model_base+'_'+variant
    #model = model_base
    for varname in vars_all:
        files = glob.glob(os.path.join(out_dir, f'{varname}.*.{year}.nc'))
        if len(files) == 1:
            continue
        if varname in vars_1:
            file_type = '3hourly'
        elif varname in vars_2 :
            file_type = 'hourly'
        else:
            file_type = '5min'

        #cmd = f'python -u postprocess.py {model} {file_type} {year} {domain} {varname} {in_dir} {out_dir} {leap_flag} {bc_flag}'
        #os.system(cmd)
        
        cmd = f'peak_memusage python -u postprocess.py {model} {file_type} {year} {domain} {varname} {in_dir} {out_dir} {leap_flag} {bc_flag} > ../logs/{variant}_{varname}_{year}.log'
        #os.system(cmd)
        newstr = f'{varname}_{year}'
        
        # Now create a new command submission script
        fo = open(pbs_orig,'r')
        lines = fo.readlines()

        pbs_new = f'pbs_{variant}_{varname}_{year}_{domain}.sh'
        fn = open(os.path.join('../sh',pbs_new),'w')

        for line in lines:
            if bogey in line:
                newline = line.replace(bogey,newstr)
                fn.writelines(newline)
            else:              
                fn.writelines(line)
        fn.writelines(cmd)
        fn.close()

        # Submit the PBS script
        directive = 'qsub %s' %(os.path.join('../sh',pbs_new))
        os.system(directive)
        
