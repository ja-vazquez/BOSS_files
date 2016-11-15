import os, sys, time
from Useful import *



N_cores = 20
threads = 5
chains_dir = 'chains_Lya/'
to_do = 'all'


if len(sys.argv) > 2:
    to_do    = sys.argv[1]
    models   = sys.argv[2].split(',')
    datasets = sys.argv[3].split(',')
else:
    Info()
    sys.exit(1)


if  'all' in models:
#   models = ['wowaCDM']
   models = ['LCDM','OkLCDM', 'woCDM', 'OkwoCDM', 'wowaCDM', 'OkwowaCDM']
if  'all' in datasets:
   datasets = ['PLK+DR12+JLA','PLK+DR12','PLK+BAO12'] 

try:
    for model in models:
        for dataset in datasets:
            TD = Tasks(model, dataset,chains_dir)

            if to_do in ['all','wini']:
                TD.write_ini()
            if to_do in ['all','wwq']:
                TD.write_wq(N_cores, threads)
            if to_do in ['all','wrun']:
                os.system('nohup wq sub  wq_%s_%s.ini &'%(model,dataset))
            if to_do in 'wdist':
                TD.write_dist()
        	os.system('./getdist distparams_%s_%s.ini'%(model, dataset))

            time.sleep(1.)
except:
    Info()
