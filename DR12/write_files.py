

import os, sys, time


def write_ini(model, dataset):
    with open('INI_' + model+ '_' + dataset + '.ini', 'w') as f:

        f.write('#Root name for files produced \n')
        f.write('file_root= %s_%s \n'%(model, dataset))

        #Select datasets

        if 'PLK' in dataset:
            f.write("""
#Planck 2015, default just include native likelihoods (others require clik)
#DEFAULT(batch2/plik_dx11dr2_HM_v18_TT.ini)
DEFAULT(batch2/plik_dx11dr2_HM_v18_TTTEEE.ini)
DEFAULT(batch2/lowTEB.ini)
#DEFAULT(batch2/lensing.ini)  \n\n""")

	if 'BAO12' in dataset: f.write('DEFAULT(batch2/DR12_blows8.ini) \n\n')
        if 'DR12'  in dataset: f.write('DEFAULT(batch2/DR12.ini) \n\n')
        if 'JLA'   in dataset: f.write('DEFAULT(batch2/JLA.ini) \n\n')

        #write main file
        f.write('DEFAULT(DR12_INI.ini) \n\n')

        #select parameters to vary

        f.write('param[omegak] = 0 %s \n'%('-0.1 0.1 0.005 0.005' if 'Ok' in model else ''))
        f.write('param[w]      = -1 %s \n'%('-2 0 0.05 0.05'   if 'w' in model else ''))
        f.write('param[mnu]    = 0.06 %s \n'%('0 2 0.1 0.1'       if 'mnu' in model else ''))
        f.write('param[nnu]    = 3.046 %s \n'%('2 6 0.1 0.1'      if 'Neff' in model else ''))
        f.write('param[Alens]  = 1 %s \n'%('0 2 0.1 0.1'          if 'Alens' in model else ''))
	f.write('param[Afs8]   = 1 %s \n'%('0 2 0.1 0.1'          if 'Afs8' in model or 'ABfs8' in model else ''))
	f.write('param[Bfs8]   = 0 %s \n'%('-2 1 0.1 0.1'         if 'ABfs8' in model else ''))

def write_wq(model, dataset):
    name = model+ '_' + dataset

    wq_input = """
mode: bycore
N: 20
threads: 5
hostfile: auto
job_name: %s
command: |
     source ~/.bashrc;
     OMP_NUM_THREADS=%%threads%% mpirun -hostfile %%hostfile%% ./cosmomc INI_%s.ini > chains_new/logs/INI_%s.log 2>chains_new/logs/INI_%s.err
    """%(name, name, name, name)

    with open('wq_' + name + '.ini', 'w') as f:
        f.write(wq_input)




def write_dist(model, dataset):
    name = model+ '_' + dataset
    i = 1
    with open('distparams_' + name + '.ini', 'w') as f:

        f.write('file_root = chains/%s \n\n'%(name))
        f.write('INCLUDE(distparams.ini) \n\n')

        f.write('plot%i = omegam H0 \n'%(i));        i+=1

        if 'Ok' in model:    f.write('plot%i = omegak H0 \n'%(i));    i+=1
        if 'w' in model:     f.write('plot%i = w H0 \n'%(i));         i+=1
        if 'mnu' in model:   f.write('plot%i = mnu H0 \n'%(i));       i+=1
        if 'Neff' in model:  f.write('plot%i = nnu H0 \n'%(i));       i+=1
        if 'Alens' in model: f.write('plot%i = Alens H0 \n'%(i));     i+=1

        f.write('plot_2D_num = %i \n\n'%(i-1))

        if dataset == 'PLK':
        #   models = model.replace('Alens_','')

            f.write('compare_num = 3 \n')
            f.write('compare1 = %s_PLK+DR12 \n'%(model))
            f.write('compare2 = %s_PLK+DR12+JLA \n'%(model))
            f.write('compare3 = Alens_%s_PLK+BAO12 \n'%(model))
        else:
            f.write('compare_num = 0 \n')



def print_info():
     print 'Usage:'
     print '---'
     print 'python write_files run/dist all/neutrino/fs8[models, datasets]'
     print '---'


# #Main code
#-------------------------------------------------------------


if sys.argv[1] == 'info':
     print_info()
     sys.exit(1)
else:
     to_do = '%s'%(sys.argv[1])

if len(sys.argv) > 2:

   if sys.argv[2] == 'all':
        modell = ['LCDM','wCDM','OkwCDM','mnu','Neff']
        datasetl = ['PLK+DR12+JLA', 'PLK+DR12', 'PLK']
   elif sys.argv[2] == 'neutrino':
        modell = ['mnu','Neff','Alens_mnu','Alens_Neff']
        datasetl = ['PLK+BAO12', 'PLK+DR12']
   elif sys.argv[2] == 'fs8':
	modell = ['Afs8_LCDM','ABfs8_LCDM']
	datasetl = ['PLK+DR12']
   elif len(sys.argv) > 3:
        modell = sys.argv[2].split(',')
        datasetl = sys.argv[3].split(',')

try:
 for model in modell:
     for dataset in datasetl:

        if to_do == 'run':
           write_ini(model, dataset)
           write_wq(model, dataset)
           os.system('nohup wq sub  wq_%s_%s.ini &'%(model,dataset))

        if to_do == 'dist':
           write_dist(model, dataset)
           os.system('./getdist distparams_%s_%s.ini'%(model, dataset))

           if dataset == 'PLK':
              os.system('python stats/%s_%s_2D.py'%(model, dataset))

        time.sleep(1.)
except:
 print_info()


