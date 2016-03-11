import os, sys, time


def write_ini(model, dataset):
    with open('INI_' + model+ '_' + dataset + '.ini', 'w') as f:
        
        f.write('#Root name for files produced \n')
        f.write('file_root= %s_%s \n'%(model, dataset))
        
        #Select datasets
        
        if 'PLK' in dataset:
            f.write("""
#Planck 2015, default just include native likelihoods (others require clik)
DEFAULT(batch2/plik_dx11dr2_HM_v18_TT.ini)
DEFAULT(batch2/lowTEB.ini)
DEFAULT(batch2/lowl.ini)
DEFAULT(batch2/lensing.ini) \n\n""")
        
        if 'DR12' in dataset:
            f.write('#DR12 BAO-RSD \n')
            f.write('DEFAULT(batch2/DR12.ini) \n\n')
            
        if 'JLA' in dataset:
            f.write('#Supernovae \n')
            f.write('DEFAULT(batch2/JLA.ini) \n\n')
            
        if 'blows8' in dataset:
            f.write('DEFAULT(batch2/DR12_blows8.ini) \n\n')

	#write main file
	f.write('DEFAULT(DR12_INI.ini) \n\n')
            
        #select parameters to vary
        
        f.write('param[omegak] = 0 %s \n'%('-0.1 0.1 0.005 0.005' if 'Ok' in model else ''))
        
        f.write('param[w]      = -1 %s \n'%('-2 0 0.05 0.05'   if 'w' in model else ''))
        
        f.write('param[mnu]    = 0.06 %s \n'%('0 2 0.1 0.1'       if 'mnu' in model else ''))
        
        f.write('param[nnu]    = 3.046 %s \n'%('2 6 0.1 0.1'      if 'Neff' in model else ''))
        
        f.write('param[Alens]  = 1 %s \n'%('0 2 0.1 0.1'          if 'Alens' in model else ''))
        
        
        
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
     OMP_NUM_THREADS=%%threads%% mpirun -hostfile %%hostfile%% ./cosmomc INI_%s.ini > chains/logs/INI_%s.log 2>chains/logs/INI_%s.err
    """%(name, name, name, name)
        
    with open('wq_' + name + '.ini', 'w') as f:
        f.write(wq_input)



modell = ['Alens_wCDM', 'Alens_OkwCDM']   #['LCDM', 'wCDM', 'OkwCDM', 'mnu', 'Neff']
datasetl = ['PLK+blows8']  #['PLK','PLK+DR12'] #,'PLK+DR12+JLA']


for model in modell:
    for dataset in datasetl:

        write_ini(model, dataset)
        write_wq(model, dataset)

        commd = """
        nohup wq sub  wq_%s_%s.ini &
        """%(model,dataset)
        os.system(commd)
        time.sleep(1.)



