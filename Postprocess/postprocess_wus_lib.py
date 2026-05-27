import netCDF4 as nc
import numpy as np
import os, glob, sys
import wrf
import time
import cftime
from datetime import datetime

# define pressure levels to interpolate
lev_p = np.array([1000, 925, 850, 800, 700, 600, 500, 400, 300, 250]) # units:hPa

# define some constants
Rd = 287.0
g = 9.81

# meta data directory
meta_dir = '/glade/work/leihuang/meta_wrf/meta_data_wus/'

#CF_variables = ['gh_sfc', 'lw_sfc', 'snow', 'sw_sfc', 'ivt', 'w_3d', 'uv10', 
#                 'cape', 'cin', 'lcl', 'lfc', 'wspd100max', 'wspd100mean', 'uv100']

# define the variables dictionary
vars_dict = {
        'evspsbl': {'nc_name':'ETRAN', 'units':'mm/d', 'long_name':'evapotranspiration at the surface', 'scale':86400.0, 
                       'missing_filter':True, 'land_filter': False},
        'es': {'nc_name':'EDIR', 'units':'mm/d', 'long_name': 'evaporation at the surface', 'scale':86400.0, 
                     'missing_filter':False, 'land_filter': False},
        'gh_sfc': {'nc_name':'GRDFLX', 'units':'W/m2', 'long_name': 'ground heat flux', 'scale':1.0, 
                   'missing_filter':True, 'land_filter': True},        
        'hfls': {'nc_name':'LH', 'units':'W/m2', 'long_name': 'surface upward latent heat flux', 'scale':1.0, 
                   'missing_filter':True, 'land_filter': True},
        'rlds': {'nc_name':'LWDNB', 'units':'W/m2', 'long_name': 'surface downwelling longwave radiation', 'scale':1.0, 
                   'missing_filter':False, 'land_filter': False},         #hourly        
        'lw_sfc': {'nc_name':'FIRA', 'units':'W/m2', 'long_name': 'longwave flux at the surface', 'scale':1.0, 
                   'missing_filter':True, 'land_filter': True},        
        'ps': {'nc_name':'PSFC', 'units':'Pa', 'long_name': 'surface air pressure', 'scale':1.0, 
                 'missing_filter':False, 'land_filter': False},
        'huss': {'nc_name':'Q2', 'units':'g/kg', 'long_name': '2-meter specific humidity', 'scale':1000.0, 
               'missing_filter':False, 'land_filter': False},        
        'hfss': {'nc_name':'HFX', 'units':'W/m2', 'long_name': 'surface upward sensible heat flux', 'scale':1.0, 
                   'missing_filter':True, 'land_filter': True},
        'mrso': {'nc_name':'SMOIS', 'units':'m3/m3', 'long_name': 'total soil moisture content', 'scale':1.0, 
                   'missing_filter':False, 'land_filter': False},
        'tsl': {'nc_name':'TSLB', 'units':'K', 'long_name': 'soil temperature', 'scale':1.0, 
                   'missing_filter':False, 'land_filter': False},
        'snow': {'nc_name':'SNOW',  'units':'mm', 'long_name': 'snow water equivalent', 'scale':1.0, 
                 'missing_filter':False, 'land_filter': False},            #hourly       
        'mrros': {'nc_name':'RUNSF', 'units':'mm/d', 'long_name': 'surface runoff', 'scale':86400.0, 
                       'missing_filter':False, 'land_filter': False},      #hourly
        'mrrob': {'nc_name':'RUNSB', 'units':'mm/d', 'long_name': 'subsurface runoff', 'scale':86400.0, 
                          'missing_filter':False, 'land_filter': False},   #hourly
        'rsds': {'nc_name':'SWDOWN', 'units':'W/m2', 'long_name': 'surface downwelling shortwave radiation', 'scale':1.0, 
                   'missing_filter':True, 'land_filter': True},
        'sw_sfc': {'nc_name':'FSA', 'units':'W/m2', 'long_name': 'shortwave flux at the surface', 'scale':1.0, 
                   'missing_filter':True, 'land_filter': True},
        'tas': {'nc_name':'T2', 'units':'K', 'long_name': '2-meter temperature', 'scale':1.0, 
               'missing_filter':False, 'land_filter': False},              #hourly
        'ts': {'nc_name':'TSK', 'units':'K', 'long_name':'surface skin temperature', 'scale':1.0, 
                  'missing_filter':False, 'land_filter': False},           #hourly
        'hurs': {'nc_name':'rh2', 'units':'%[0 to 100]', 'long_name': '2-meter relative humidity', 'scale':1.0, 
               'missing_filter':False, 'land_filter': False},
        'ivt': {'nc_name':'', 'units':'kg/s/m [0 for u, 1 for v]', 'long_name': 'integrated water vapor transport', 'scale':1.0, 
                'missing_filter':False, 'land_filter': False},
        'clivi': {'nc_name':'', 'units':'kg/m2', 'long_name': 'ice water path', 'scale':1.0, 
                'missing_filter':False, 'land_filter': False},
        'lwp': {'nc_name':'', 'units':'kg/m2', 'long_name': 'liquid water path', 'scale':1.0, 
                'missing_filter':False, 'land_filter': False},
        'zg': {'nc_name':'geopt', 'units':'m2/s2', 'long_name': 'geopotential height', 'scale':1.0, 
                   'missing_filter':False, 'land_filter': False},
        'ta': {'nc_name':'tk', 'units':'K', 'long_name': 'air temperature on pressure levels', 'scale':1.0, 
                 'missing_filter':False, 'land_filter': False},
        'hus': {'nc_name':'QVAPOR', 'units':'g/kg', 'long_name': 'specific humidity on pressure levels', 'scale':1000.0, 
                 'missing_filter':False, 'land_filter': False}, 
        'ua': {'nc_name':'uvmet', 'units':'m/s', 'long_name': 'eastward wind on pressure levels', 'scale':1.0, 
                 'missing_filter':False, 'land_filter': False},
        'va': {'nc_name':'uvmet', 'units':'m/s', 'long_name': 'northward wind on pressure levels', 'scale':1.0, 
                 'missing_filter':False, 'land_filter': False},
        'w_3d': {'nc_name':'wa', 'units':'m/s', 'long_name': 'vertical wind on pressure levels', 'scale':1.0, 
                 'missing_filter':False, 'land_filter': False},
        'uv10': {'nc_name':'', 'units':'m/s [0 for u, 1 for v]', 'long_name': '10-meter u and v wind', 'scale':1.0, 
                 'missing_filter':False, 'land_filter': False},            #hourly 
        'tasmax': {'nc_name':'T2', 'units':'K', 'long_name': 'daily maximum 2-m temperature', 'scale':1.0, 
                  'missing_filter':False, 'land_filter': False},           #hourly
        'tasmin': {'nc_name':'T2', 'units':'K', 'long_name': 'daily minimum 2-m temperature', 'scale':1.0, 
                  'missing_filter':False, 'land_filter': False},           #hourly  
        'sfcWindmax': {'nc_name':'U10', 'units':'m/s', 'long_name': 'maximum 10-meter wind speed', 'scale':1.0, 
                      'missing_filter':False, 'land_filter': False},       #hourly
        'sfcWind': {'nc_name':'U10', 'units':'m/s', 'long_name': 'mean 10-meter wind speed', 'scale':1.0, 
                       'missing_filter':False, 'land_filter': False},      #hourly
        'prc': {'nc_name':'RAINNC', 'units':'mm/d', 'long_name': 'convective precipitation', 'scale':1.0, 
                   'missing_filter':False, 'land_filter': False}, 
        'pr': {'nc_name':'RAINNC', 'units':'mm/d', 'long_name': 'total precipitation', 'scale':1.0, 
                 'missing_filter':False, 'land_filter': False},
        'prsn': {'nc_name':'SNOWNC', 'units':'mm/d', 'long_name': 'snow precipitation', 'scale':1.0, 
                      'missing_filter':False, 'land_filter': False},       #hourly    
        'prhmax': {'nc_name':'RAINNC', 'units':'mm/h', 'long_name': 'maximum hourly precipitation', 'scale':1.0, 
                     'missing_filter':False, 'land_filter': False},         #hourly
        'zmla':{'nc_name':'PBLH', 'units':'m', 'long_name': 'planetary boundary layer height', 'scale':1.0, 
                'missing_filter':False, 'land_filter': False},        
        'cape':{'nc_name':'cape_2d', 'units':'J/kg', 'long_name': 'convective available potential energy', 'scale':1.0, 
                'missing_filter':True, 'land_filter': False}, 
        'cin':{'nc_name':'cape_2d', 'units':'J/kg', 'long_name': 'convective inhibition', 'scale':1.0, 
               'missing_filter':True, 'land_filter': False}, 
        'lcl':{'nc_name':'cape_2d', 'units':'m', 'long_name': 'lifting condensation level', 'scale':1.0, 
               'missing_filter':True, 'land_filter': False}, 
        'lfc':{'nc_name':'cape_2d', 'units':'m', 'long_name': 'level of free convection', 'scale':1.0, 
               'missing_filter':True, 'land_filter': False}, 
        'irri': {'nc_name':'IRSIVOL', 'units':'mm/d', 'long_name': 'sprinkler irrigation water accumulated', 'scale':1.0, 
                 'missing_filter':False, 'land_filter': False},
        'wspd100max': {'nc_name':'U_ZL', 'units':'m/s', 'long_name': 'maximum 100-meter wind speed', 'scale':1.0, 
                      'missing_filter':False, 'land_filter': False},       #hourly
        'wspd100mean': {'nc_name':'U_ZL', 'units':'m/s', 'long_name': 'mean 100-meter wind speed', 'scale':1.0, 
                       'missing_filter':False, 'land_filter': False},      #hourly
        'uv100': {'nc_name':'', 'units':'m/s [0 for u, 1 for v]', 'long_name': '100-meter u and v wind', 'scale':1.0, 
                 'missing_filter':False, 'land_filter': False},             #hourly 
        'rlut': {'nc_name':'OLR', 'units':'W/m2', 'long_name': 'TOA outgoing longwave radiation', 'scale':1.0, 
                 'missing_filter':False, 'land_filter': False},
        'rh2max': {'nc_name':'rh2', 'units':'%[0 to 100]', 'long_name': 'daily maximum 2-m relative humidity', 'scale':1.0, 
                  'missing_filter':False, 'land_filter': False},           #hourly
        'rh2min': {'nc_name':'rh2', 'units':'%[0 to 100]', 'long_name': 'daily minimum 2-m relative humidity', 'scale':1.0, 
                  'missing_filter':False, 'land_filter': False},           #hourly
        'prec_max15min': {'nc_name':'RAINNC', 'units':'mm/h', 'long_name': 'maximum 15-min precipitation', 'scale':1.0, 
                     'missing_filter':False, 'land_filter': False},         
        'prec_max30min': {'nc_name':'RAINNC', 'units':'mm/h', 'long_name': 'maximum 30-min precipitation', 'scale':1.0, 
                     'missing_filter':False, 'land_filter': False}, 
        'prec_max60min': {'nc_name':'RAINNC', 'units':'mm/h', 'long_name': 'maximum 60-min precipitation', 'scale':1.0, 
                     'missing_filter':False, 'land_filter': False}         
        }

cape_vars = ['cape', 'cin', 'lcl', 'lfc']

def get_one_year_files(file_dir, prefix, year):
    ''' Get all the files for one year '''
    all_files = []
    os.chdir(file_dir)
    for mi in range (12):
        month = mi+1
        if month < 9:
            all_files.extend(glob.glob(f'{prefix}*{year+1:04}-{month:02}*'))
        else:
            all_files.extend(glob.glob(f'{prefix}*{year:04}-{month:02}*'))
    all_files.extend(glob.glob(f'{prefix}*{year+1:04}-09-01_00:00:00'))
    all_files = sorted(all_files)
    return all_files

def get_files(root_dir,model,file_type,year,domain,organized=True,noleap=False,nobc=True):
    ''' Get the 3hourly or hourly file list '''
    # Get the path to the wrf output files
    
    if organized:
        if nobc == False:
            model_path = os.path.join(root_dir,model+'_bc',file_type,str(year),domain)
        else:
            model_path = os.path.join(root_dir,model,file_type,str(year),domain)
    else:
        os.chdir(root_dir)
        dir_name = glob.glob('*_%s' %(str(year)))
        model_path = os.path.join(root_dir,dir_name[0],domain)
        #model_path = os.path.join(root_dir,dir_name[0])
        
    #model_path = root_dir
    print(model_path)
    os.chdir(model_path)
    # Get the list of the wrf output files
    if file_type == '3hourly':
        files = get_one_year_files(model_path, 'wrf3d', year)
    elif file_type == 'hourly':
        files = get_one_year_files(model_path, 'wrf2d', year)
    elif file_type == '5min':
        files = get_one_year_files(model_path, 'wrf5min', year)
    # Checking if the given year is a leap year  
    if noleap == False and (((year+1) % 400 == 0) or ((year+1) % 100 != 0 and (year+1) % 4 ==0)):
        ndays = 365
    else:
        ndays = 365
    correct_cnt = ndays+1
    #print(files)
    count = len(files)
    print(f'Year: {year}  Number of {file_type} files found:', count)
    if count != correct_cnt:
        error_str = f'Year: {year} Number of {file_type} files {count} is not correct. Correct number should be {correct_cnt}.'
        sys.exit(error_str)        
            
    return (files, ndays)

def get_freq(file_type):
    ''' get the temporal frequency '''
    file_num = 1
    if file_type == 'hourly':
        time_num = 24
    if file_type == '3hourly':
        time_num = 8
    else:
        time_num = 288  # 5-min
        
    return (file_num, time_num)

def get_dates(ndays, file_list, file_type, noleap):
    ''' Get the daily dates and convert to integers '''
    file_num, time_num = get_freq(file_type)
    day_cnt = 0
    dates = np.zeros(ndays)
    if noleap == False:
        cal = 'proleptic_gregorian' 
    else:
        cal = '365_day'
    epoch = cftime.datetime(1850, 1, 1, calendar=cal)
    for i in range(ndays):
        files = file_list[file_num*day_cnt:file_num*(day_cnt+1)]       
        # Get the date string       
        date_str = files[0]
        if file_type == 'hourly' or file_type == '3hourly': # wrd2d_* or wrf3d_*
            year = int(date_str[10:14]) 
            month = int(date_str[15:17]) 
            day = int(date_str[18:20])
        else:  # wrf5min_*
            year = int(date_str[12:16]) 
            month = int(date_str[17:19]) 
            day = int(date_str[20:22])
        dt_obj = cftime.datetime(year, month, day, calendar=cal)
        dates[i] = int((dt_obj - epoch).days)
        day_cnt += 1
        
    return dates

def add_new_variables(nc_data, meta_data, nc_file, wrf2d=True):
    ''' Add static variables and time-dependent variables '''
    if wrf2d == True:
        nc_data.variables['XLAT'] = meta_data.variables['XLAT']
        nc_data.variables['XLONG'] = meta_data.variables['XLONG']
        nc_data.variables['LANDMASK'] = meta_data.variables['LANDMASK']
    else:
        nc_data.variables['XLAT'] = meta_data.variables['XLAT']        
        nc_data.variables['XLONG'] = meta_data.variables['XLONG']
        PH = nc_data.variables['PH'][:]  
        time_len = PH.shape[0]            
        # Broadcast PHB, PB from time=1 to the time dimension in PH
        PHB_meta = meta_data.variables['PHB'][:]
        PHB = np.broadcast_to(PHB_meta, (time_len,) + PHB_meta.shape[1:])
        nc_data.variables['PHB'] = PHB
        PB_meta = meta_data.variables['PB'][:]
        PB = np.broadcast_to(PB_meta, (time_len,) + PB_meta.shape[1:])
        nc_data.variables['PB'] = PB
        HGT_meta = meta_data.variables['HGT'][:]
        HGT = np.broadcast_to(HGT_meta, (time_len,) + HGT_meta.shape[1:])
        nc_data.variables['HGT'] = HGT
                
        # Get PSFC from the corresponding wrf2d file
        file_2d = nc_file.replace('3d', '2d')
        try:
            with nc.Dataset(file_2d) as ds_2d:
                tmp = ds_2d.variables['PSFC'][:]
                PSFC = tmp[[0, 3, 6, 9, 12, 15, 18, 21], ...] # subsample from hourly file to match 3-hourly data
                #print(PSFC.shape, PH.shape)
        except Exception as e:
            sys.exit(f"Failed to open wrf2d file: {file_2d}\n{e}")            
        nc_data.variables['PSFC'] = PSFC

    return # no reassignment, modifies nc_data in place
      
def get_uv_mass(wrf_files, domain, height):
    ''' Calculate the u and v winds at a specific height on mass points'''
    meta_file = os.path.join(meta_dir, 'wrfinput_'+domain)
    cosalpha = wrf.getvar(nc.Dataset(meta_file), 'COSALPHA', meta=False)
    sinalpha = wrf.getvar(nc.Dataset(meta_file), 'SINALPHA', meta=False)
    dims = cosalpha.shape
    #num = len(wrf_files)
    num = 24 
    uu = np.zeros((num,dims[0],dims[1]))
    vv = np.zeros((num,dims[0],dims[1]))
    if height == 10:
        u = wrf.getvar(nc.Dataset(wrf_files[0]), 'U10', timeidx=wrf.ALL_TIMES, meta=False)
        v = wrf.getvar(nc.Dataset(wrf_files[0]), 'V10', timeidx=wrf.ALL_TIMES, meta=False)
    if height == 100:
        u = wrf.getvar(nc.Dataset(wrf_files[0]), 'U_ZL', timeidx=wrf.ALL_TIMES, meta=False)
        v = wrf.getvar(nc.Dataset(wrf_files[0]), 'V_ZL', timeidx=wrf.ALL_TIMES, meta=False)
    for j in range(num):
        uu[j,:,:] = u[j,:,:]*cosalpha - v[j,:,:]*sinalpha
        vv[j,:,:] = v[j,:,:]*cosalpha + u[j,:,:]*sinalpha
        
    return(uu,vv)
    
def get_daily_mean(varname, ndays, file_list, file_type, domain):
    ''' Calculate the daily average of the input variable '''
    # get the variable name in the netcdf file
    var_ncname = vars_dict[varname]['nc_name']
    # check if need to set missing value to zero
    missing_filter = vars_dict[varname]['missing_filter']
    # check if need to read land flags
    land_filter = vars_dict[varname]['land_filter']
    # Load meta variables from wrfinput file
    meta_file = os.path.join(meta_dir, f'wrfinput_{domain}')
    meta_data = nc.Dataset(meta_file)
    
    file_num, time_num = get_freq(file_type)
    day_cnt = 0
    for i in range(ndays):
        files = file_list[file_num*day_cnt:file_num*(day_cnt+1)]
        #print(i, files)
        if i == 0:
            tmp = wrf.getvar(nc.Dataset(files[0]), var_ncname, timeidx=0, meta=False)
            dims = tmp.shape
            if len(dims) == 2:
                var_data = np.zeros((time_num,dims[0],dims[1]))
                var_daily = np.zeros((ndays,dims[0],dims[1]))
            elif len(dims) == 3:
                var_data = np.zeros((time_num,dims[1],dims[2]))
                var_daily = np.zeros((ndays,dims[1],dims[2]))
            else:
                print('Incorrect variable dimensions!')
                
        # calculate daily average of variable
        if varname == 'wspd10mean':
            uu, vv = get_uv_mass(files, domain, 10)
            var_data = np.sqrt(np.square(uu) + np.square(vv))
        elif varname == 'wspd100mean':
            uu, vv = get_uv_mass(files, domain, 100)
            var_data = np.sqrt(np.square(uu) + np.square(vv))
        else:
            nc_data = nc.Dataset(files[0])
            add_new_variables(nc_data, meta_data, files[0], True)
            var_data = wrf.getvar(nc_data, var_ncname, timeidx=wrf.ALL_TIMES, meta=False)
            land = wrf.getvar(nc_data, 'LANDMASK', timeidx=0, meta=False)
            nc_data.close()  
        var_mean = var_data.mean(axis=0) 
        if missing_filter == True:
            var_mean = np.where(abs(var_mean) > 1e+10, 0., var_mean)
        if land_filter == True:
            var_mean = np.where(land < 1, 1.e+30, var_mean)
        var_mean = var_mean * vars_dict[varname]['scale']
        var_daily[i,:,:] = var_mean
        day_cnt = day_cnt + 1
        print('day_cnt = ', day_cnt)
    meta_data.close()
    
    return var_daily

def get_rho_dz(wrfdata):
    ''' Calculate air density '''
    p = wrf.getvar(wrfdata, 'pres', timeidx=wrf.ALL_TIMES)
    tk = wrf.getvar(wrfdata, 'tk', timeidx=wrf.ALL_TIMES)
    z = wrf.getvar(wrfdata, 'z', timeidx=wrf.ALL_TIMES)
    rho = (p / Rd) / tk
    dims = z.shape
    dz = np.zeros(dims)   
    # top layer is neglected
    for iz in range(dims[1]-1):
        dz[:,iz,:,:] = z[:,iz+1,:,:] - z[:,iz,:,:]
    
    return (rho, dz)
    
def get_daily_mean_ivt(ndays, file_list, file_type, domain):
    ''' Calculate the daily average of ivt ''' 
    # Load meta variables from wrfinput file
    meta_file = os.path.join(meta_dir, f'wrfinput_{domain}')
    meta_data = nc.Dataset(meta_file)
    file_num, time_num = get_freq(file_type)
    day_cnt = 0
    for i in range(ndays):
        files = file_list[day_cnt:day_cnt+1]
        nc_data = nc.Dataset(files[0])
        add_new_variables(nc_data, meta_data, files[0], False)

        # calculate daily average of variable
        wind = wrf.getvar(nc_data, 'uvmet', timeidx=wrf.ALL_TIMES)
        q = wrf.getvar(nc_data, 'QVAPOR', timeidx=wrf.ALL_TIMES)       
        rho, dz = get_rho_dz(nc_data)
        nc_data.close()
           
        # compute ivt for u and v
        ivt_u = (rho * wind[0,:,:,:,:] * q * dz).sum(axis=1)
        ivt_v = (rho * wind[1,:,:,:,:] * q * dz).sum(axis=1)
        
        if i == 0:
            dims = q.shape
            var_daily = np.zeros((ndays,2,dims[2],dims[3]))

        var_daily[i,0,:,:] = ivt_u.mean(axis=0)
        var_daily[i,1,:,:] = ivt_v.mean(axis=0)
        day_cnt = day_cnt + 1
        print('day_cnt = ', day_cnt)
    meta_data.close()
    
    return var_daily

def get_daily_mean_uv(ndays, file_list, file_type, domain, height):
    ''' Calculate the daily average of 10-meter u and v wind ''' 
    file_num, time_num = get_freq(file_type)
    day_cnt = 0
    for i in range(ndays):
        files = file_list[file_num*day_cnt:file_num*(day_cnt+1)]
        uu, vv = get_uv_mass(files, domain, height)
        if i == 0:         
            dims = uu.shape
            var_daily = np.zeros((ndays,2,dims[1],dims[2]))
            
        # calculate daily average of variable
        var_daily[i,0,:,:] = uu.mean(axis=0)
        var_daily[i,1,:,:] = vv.mean(axis=0)
        day_cnt = day_cnt + 1
        print('day_cnt = ', day_cnt)
        
    return var_daily
    
def get_daily_mean_wp(varname, ndays, file_list, file_type, domain):
    ''' Calculate the daily average of iwp or lwp ''' 
    # Load meta variables from wrfinput file
    meta_file = os.path.join(meta_dir, f'wrfinput_{domain}')
    meta_data = nc.Dataset(meta_file)
    file_num, time_num = get_freq(file_type) 
    day_cnt = 0
    for i in range(ndays):
        files = file_list[file_num*day_cnt:file_num*(day_cnt+1)]       
        nc_data = nc.Dataset(files[0])
        add_new_variables(nc_data, meta_data, files[0], False)
        
        # calculate daily average of variable
        rho, dz = get_rho_dz(nc_data)
        if varname == 'clivi':
            q = wrf.getvar(nc_data, 'QICE', timeidx=wrf.ALL_TIMES) 
        else:
            q = wrf.getvar(nc_data, 'QCLOUD', timeidx=wrf.ALL_TIMES) + wrf.getvar(nc_data, 'QRAIN', timeidx=wrf.ALL_TIMES)
        nc_data.close()
        
        # compute iwp or lwp
        wp = (rho * q * dz).sum(axis=1)
        
        if i == 0:
            dims = q.shape
            var_daily = np.zeros((ndays,dims[2],dims[3]))

        var_daily[i,:,:] = wp.mean(axis=0)
        day_cnt = day_cnt + 1
        print('day_cnt = ', day_cnt)
    meta_data.close()
    
    return var_daily

def get_daily_mean_cape(varname, ndays, file_list, file_type, domain):
    ''' Calculate the daily average of cape, cin, lcl, and lfc '''
    # Load meta variables from wrfinput file
    meta_file = os.path.join(meta_dir, f'wrfinput_{domain}')
    meta_data = nc.Dataset(meta_file)
    file_num, time_num = get_freq(file_type)
    # get the variable name in the netcdf file
    var_ncname = vars_dict[varname]['nc_name']
    # check if need to set missing value to zero
    missing_filter = vars_dict[varname]['missing_filter']
    # check if need to read land flags
    land_filter = vars_dict[varname]['land_filter']
    
    day_cnt = 0
    
    for i in range(ndays):
        files = file_list[file_num*day_cnt:file_num*(day_cnt+1)]
        nc_data = nc.Dataset(files[0])
        add_new_variables(nc_data, meta_data, files[0], False)      

        # calculate daily average of variable
        var = wrf.getvar(nc_data, var_ncname, timeidx=wrf.ALL_TIMES)
        #print(var.shape)
        index = cape_vars.index(varname)
        var2 = var[index,:,:,:]
        nc_data.close()

        # Allocate memory on first loop
        if i == 0:
            dims = var.shape
            var_daily = np.zeros((ndays,dims[2],dims[3]))

        # Average over time dimension and store result
        var_mean = var2.mean(axis=0) 
        if missing_filter == True:
            var_mean = np.where(abs(var_mean) > 1e+10, 0., var_mean)
        if land_filter == True:
            var_mean = np.where(land < 1, 1.e+30, var_mean)
        var_mean *= vars_dict[varname]['scale']
        var_daily[i,:,:] = var_mean
        day_cnt = day_cnt + 1
        print('day_cnt = ', day_cnt)
    meta_data.close()
    
    return var_daily
    
    
def get_daily_mean_soil(varname, ndays, file_list, file_type):
    ''' Calculate the daily average of soil_m or soil_t ''' 
    # get the variable name in the netcdf file
    var_ncname = vars_dict[varname]['nc_name']
    
    file_num, time_num = get_freq(file_type) 
    day_cnt = 0
    for i in range(ndays):
        files = file_list[file_num*day_cnt:file_num*(day_cnt+1)]
        if i == 0:
            tmp = wrf.getvar(nc.Dataset(files[0]), var_ncname, timeidx=0, meta=False)
            dims = tmp.shape
            var_data = np.zeros((time_num,dims[0],dims[1],dims[2]))
            var_daily = np.zeros((ndays,dims[0],dims[1],dims[2]))
                    
        # calculate daily average of variable
        var_data = wrf.getvar(nc.Dataset(files[0]), var_ncname, timeidx=wrf.ALL_TIMES, meta=False)   
        var_mean = var_data.mean(axis=0) 
        var_mean *= vars_dict[varname]['scale']
        var_daily[i,:,:,:] = var_mean
        day_cnt = day_cnt + 1
        print('day_cnt = ', day_cnt)
        
    return var_daily
    
def get_daily_mean_3d(varname, ndays, file_list, file_type, domain):
    ''' Calculate the daily average of 3d variables ''' 
    # Load meta variables from wrfinput file
    meta_file = os.path.join(meta_dir, f'wrfinput_{domain}')
    meta_data = nc.Dataset(meta_file)
    file_num, time_num = get_freq(file_type)
    # get the variable name in the netcdf file
    var_ncname = vars_dict[varname]['nc_name']
    day_cnt = 0
    
    for i in range(ndays):
        files = file_list[file_num*day_cnt:file_num*(day_cnt+1)]
        nc_data = nc.Dataset(files[0])
        add_new_variables(nc_data, meta_data, files[0], False)         

        # calculate daily average of variable
        var = wrf.getvar(nc_data, var_ncname, timeidx=wrf.ALL_TIMES)
        if varname == 'ua':
            var = var[0,:,:,:,:]
        elif varname == 'va':
            var = var[1,:,:,:,:]
        var_interp = wrf.vinterp(nc_data, field=var, vert_coord='pressure', interp_levels=lev_p, 
                                 extrapolate=False, field_type='pressure', log_p=True, timeidx=wrf.ALL_TIMES)
        nc_data.close()
        
        # Allocate memory on first loop
        if i == 0:
            dims = var.shape
            var_daily = np.zeros((ndays,len(lev_p),dims[2],dims[3]))

        # Average over time dimension and store result
        var_daily[i,:,:,:] = var_interp.mean(axis=0) * vars_dict[varname]['scale']
        day_cnt = day_cnt + 1
        print('day_cnt = ', day_cnt)
        
    meta_data.close()
    
    return var_daily

def get_daily_minmax(varname, ndays, file_list, file_type, domain):
    ''' Calculate the daily min/max of variables ''' 
    file_num, time_num = get_freq(file_type)  
    day_cnt = 0
    # get the variable name in the netcdf file
    var_ncname = vars_dict[varname]['nc_name']
    
    for i in range(ndays):
        files = file_list[file_num*day_cnt:file_num*(day_cnt+1)]
        if i == 0:
            tmp = wrf.getvar(nc.Dataset(files[0]), var_ncname, timeidx=0, meta=False)
            dims = tmp.shape
            var_data = np.zeros((time_num,dims[0],dims[1]))
            var_daily = np.zeros((ndays,dims[0],dims[1]))
        if varname == 'wspd10max' or varname == 'wspd10min':
            uu, vv = get_uv_mass(files, domain, 10)
            var_data = np.sqrt(np.square(uu) + np.square(vv))
        elif varname == 'wspd100max' or varname == 'wspd100min':
            uu, vv = get_uv_mass(files, domain, 100)
            var_data = np.sqrt(np.square(uu) + np.square(vv))
        else:
            if file_num == 1: 
                var_data = wrf.getvar(nc.Dataset(files[0]), var_ncname, timeidx=wrf.ALL_TIMES, meta=False)  
            else:
                for j in range(time_num):
                    var_data[j,:,:] = wrf.getvar(nc.Dataset(files[j]), var_ncname, timeidx=0, meta=False)
        
        if 'min' in varname:
            var_daily[i,:,:] = var_data.min(axis=0) * vars_dict[varname]['scale']
        else:
            var_daily[i,:,:] = var_data.max(axis=0) * vars_dict[varname]['scale']
        day_cnt = day_cnt + 1
        print('day_cnt = ', day_cnt)
        
    return var_daily

def get_prec_max_interval(varname, ndays, file_list, file_type, domain):
    ''' Calculate the hourly precipitation min/max ''' 
    meta_file = os.path.join(meta_dir, f'wrfinput_{domain}')
    meta_data = nc.Dataset(meta_file)
    file_num, time_num = get_freq(file_type) 
    day_cnt = 0
    # get the variable name in the netcdf file
    var_ncname = vars_dict[varname]['nc_name']
    try:
        interval = int(varname[-5:-3])
    except Exception as e:
        sys.exit(f"Time interval is not valid.\n{e}")
    multiplier = 60 // interval
           
    for i in range(ndays):
        files = file_list[file_num*day_cnt:file_num*(day_cnt+1)+1]
        if i == 0:
            tmp = wrf.getvar(nc.Dataset(files[0]), var_ncname, timeidx=0, meta=False)
            dims = tmp.shape
            var_daily = np.zeros((ndays,dims[0],dims[1]))

        nc_data = nc.Dataset(files[0])
        nc_data.variables["XLAT"] = meta_data.variables["XLAT"]
        nc_data.variables["XLONG"] = meta_data.variables["XLONG"]
        d1 = wrf.getvar(nc_data, 'RAINNC', timeidx=wrf.ALL_TIMES)
        if 'RAINC' in nc.Dataset(files[0]).variables.keys():
            d2 = wrf.getvar(nc_data, 'RAINC', timeidx=wrf.ALL_TIMES)
            prec = d1 + d2
        else:
            prec = d1
        # Get the maximum precipitation in each interval time window
        prec_max_interval = prec.diff(dim='Time').resample(Time=f'{interval}min').sum()
        prec_max_interval = prec_max_interval * multiplier # convert (mm/interval) to mm/hr
        # Get the daily maximum
        var_daily[i,:,:] = prec_max_interval.max(axis=0) * vars_dict[varname]['scale']
        day_cnt = day_cnt + 1
        print('day_cnt = ', day_cnt)
        nc_data.close()
    meta_data.close()
        
    return var_daily

def get_precipitation(varname, ndays, file_list, file_type):
    ''' Calculate the daily/hourly precipitation ''' 
    file_num, time_num = get_freq(file_type)  
    day_cnt = 0
    # get the variable name in the netcdf file
    var_ncname = vars_dict[varname]['nc_name']
    
    for i in range(ndays):
        files = file_list[file_num*day_cnt:file_num*(day_cnt+1)+1]
        if i == 0:
            tmp = wrf.getvar(nc.Dataset(files[0]), var_ncname, timeidx=0, meta=False)
            dims = tmp.shape
            var_daily = np.zeros((ndays,dims[0],dims[1]))       
       
        # calculate daily/hourly accumulated precipitation
        if varname == 'pr':
            if 'RAINC' in nc.Dataset(files[0]).variables.keys():
                var_daily[i,:,:] = wrf.getvar(nc.Dataset(files[file_num]), 'RAINNC', meta=False) - wrf.getvar(nc.Dataset(files[0]), 'RAINNC', meta=False) + \
                               wrf.getvar(nc.Dataset(files[file_num]), 'RAINC', meta=False) - wrf.getvar(nc.Dataset(files[0]), 'RAINC', meta=False)
            else:
                var_daily[i,:,:] = wrf.getvar(nc.Dataset(files[file_num]), 'RAINNC', meta=False) - wrf.getvar(nc.Dataset(files[0]), 'RAINNC', meta=False)
        elif varname == 'prc':
            if 'RAINC' in nc.Dataset(files[0]).variables.keys():
                var_daily[i,:,:] = wrf.getvar(nc.Dataset(files[file_num]), 'RAINC', meta=False) - wrf.getvar(nc.Dataset(files[0]), 'RAINC', meta=False)
            else:
                var_daily[i,:,:] = 0
        elif varname == 'irri':
            var_daily[i,:,:] = wrf.getvar(nc.Dataset(files[file_num]), 'IRSIVOL', meta=False) - wrf.getvar(nc.Dataset(files[0]), 'IRSIVOL', meta=False)
        elif varname == 'prsn':
            d1 = wrf.getvar(nc.Dataset(files[0]), 'SNOWNC', timeidx=wrf.ALL_TIMES, meta=False)
            d2 = wrf.getvar(nc.Dataset(files[1]), 'SNOWNC', timeidx=wrf.ALL_TIMES, meta=False)
            #print(d1.shape, d2.shape)
            if d2.ndim == 2:
                var_daily[i,:,:] = d2 - d1[0,:,:]   # Last file only has one-hour data
            else:
                var_daily[i,:,:] = d2[0,:,:] - d1[0,:,:]
        day_cnt = day_cnt + 1
        print('day_cnt = ', day_cnt)
        
    return var_daily

def write_nc(in_file, out_file, varname, var_daily, dates, lats, lons, dim3='', noleap=False):
    ''' Write the variable daily values and dates to a netcdf file '''
    # Delete the outfile if already existed
    if os.path.exists(out_file):
        os.remove(out_file)
    
    # get the number of days
    ndays = len(dates)
    
    with nc.Dataset(in_file, 'r') as src, nc.Dataset(out_file, 'w') as dst:
        # copy global attributes all at once via dictionary
        dst.setncatts(src.__dict__)
        dst.title = varname
        dst.creation_date = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        
        nlon = len(src.dimensions['west_east'])
        nlat = len(src.dimensions['south_north']) 

        # create dimensions and variables
        dst.createDimension('time', ndays)
        dst.createDimension('lon2d', nlon)
        dst.createDimension('lat2d', nlat)
        if dim3 == 'pressure':
            dst.createDimension('pressure', len(lev_p))
            var = dst.createVariable(varname, 'f4', ('time', 'pressure', 'lat2d', 'lon2d',), fill_value=1.e+30)
            pres = dst.createVariable('pressure', 'i4', ('pressure',), fill_value=-2147483647)
            pres[:] = lev_p
            pres.units = 'hPa'
            pres.long_name = 'pressure level'
        elif dim3 == 'component':
            dst.createDimension('component', 2)
            var = dst.createVariable(varname, 'f4', ('time', 'component', 'lat2d', 'lon2d',), fill_value=1.e+30)
        elif dim3 == 'soil_nz':
            dst.createDimension('soil_nz', 4)
            var = dst.createVariable(varname, 'f4', ('time', 'soil_nz', 'lat2d', 'lon2d',), fill_value=1.e+30)
        else:
            var = dst.createVariable(varname, 'f4', ('time', 'lat2d', 'lon2d',), fill_value=1.e+30)

        var[:] = var_daily
        var.units = vars_dict[varname]['units']
        var.long_name = vars_dict[varname]['long_name']

        # Create the time variable (use "tm" to avoid conflict with "time" module)
        tm = dst.createVariable('time', 'i4', ('time',), fill_value=-2147483647)
        tm[:] = dates
        tm.units = 'days since 1850-01-01 00:00:00'
        tm.long_name = 'time'
        if noleap == False:
            tm.calendar = 'proleptic_gregorian' 
        else:
            tm.calendar = '365_day'
        
        # Create the latitude and longitude variables
        lat = dst.createVariable('latitude', 'f4', ('lat2d', 'lon2d',), fill_value=1.e+30)
        lat[:] = lats
        lat.units = 'degree_north'
        lat.long_name = 'latitude, south is negative'
        lon = dst.createVariable('longitude', 'f4', ('lat2d', 'lon2d',), fill_value=1.e+30)
        lon[:] = lons
        lon.units = 'degree_east'
        lon.long_name = 'longitude, west is negative'
        
        # add new variables here if needed (lon2d, lat2d, etc.)
        # pass

def process(model, file_type, year, domain, varname, in_dir, out_dir, noleap, nobc):
    ''' Post-process a variable for a given model, domain, and year '''
    
    var_3d = ['zg', 'hus', 'ta', 'ua', 'va', 'w_3d']    
    start_time = time.time()

    meta_file = os.path.join(meta_dir, 'wrfinput_'+domain)
    meta_data = nc.Dataset(meta_file)
    lats = wrf.getvar(meta_data, 'XLAT', timeidx=0, meta=False)
    lons = wrf.getvar(meta_data, 'XLONG', timeidx=0, meta=False)
    meta_data.close()
    
    # Get the 3hourly or hourly file list 
    print('Get the '+file_type+' file list...')
    organized = True
    if 'WRF/test' in in_dir:
        organized = False       
    files, ndays = get_files(in_dir,model,file_type,year,domain,organized,noleap,nobc)
    #print(files)
    #print(os.getcwd())
    
    # Get the daily mean values of variable and dates (as integers)
    print('Calculating the daily average...')
    dim3 = ''
    if varname == 'ivt':
        dim3 = 'component'
        var_daily = get_daily_mean_ivt(ndays, files, file_type, domain)
    elif varname == 'uv10':
        dim3 = 'component'
        var_daily = get_daily_mean_uv(ndays, files, file_type, domain, 10)
    elif varname == 'uv100':
        dim3 = 'component'
        var_daily = get_daily_mean_uv(ndays, files, file_type, domain, 100)
    elif varname == 'mrso' or varname == 'tsl':
        dim3 = 'soil_nz'
        var_daily = get_daily_mean_soil(varname, ndays, files, file_type)
    elif varname == 'clivi' or varname == 'lwp':
        var_daily = get_daily_mean_wp(varname, ndays, files, file_type, domain)
    elif varname in cape_vars:
        var_daily = get_daily_mean_cape(varname, ndays, files, file_type, domain)
    elif 'prec_max' in varname:
        var_daily = get_prec_max_interval(varname, ndays, files, file_type, domain)
    elif varname == 'pr' or varname == 'prc' or varname == 'prsn':
        var_daily = get_precipitation(varname, ndays, files, file_type)
    elif 'min' in varname or 'max' in varname:
        var_daily = get_daily_minmax(varname, ndays, files, file_type, domain)
    elif varname in var_3d:
        dim3 = 'pressure'
        var_daily = get_daily_mean_3d(varname, ndays, files, file_type, domain)
    else:
        var_daily = get_daily_mean(varname, ndays, files, file_type, domain)
    dates = get_dates(ndays, files, file_type, noleap)
    print(var_daily.shape, dates.shape)
    
    # Write the daily mean values to a netcdf file
    print('Writing the daily mean values to a netcdf file...')
    in_file = files[0]
    model = model.replace('_', '.')
    if 'historical' in model:
        model = model.replace('historical', 'hist')
    if nobc == False:
        out_file = os.path.join(out_dir, f'{varname}.daily.{model}.bias-correct.{domain}.{year}.nc')
    else:
        out_file = os.path.join(out_dir, f'{varname}.daily.{model}.{domain}.{year}.nc')
    write_nc(in_file, out_file, varname, var_daily, dates, lats, lons, dim3, noleap)
    print("--- Total time: %.2f seconds ---" % (time.time() - start_time))