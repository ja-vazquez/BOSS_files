import os, sys, time
from tasks import *



N_cores = 20
threads = 5
chains_dir = 'chains/'
to_do = 'all'

if len(sys.argv) > 2:
    models   = sys.argv[1].split(',')
    datasets = sys.argv[2].split(',')
    if len(sys.argv) > 3:
        to_do = sys.argv[3]
else:
    Info()
    sys.exit(1)


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
