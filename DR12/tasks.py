

class Info():
    def __init__(self):
        print 'Usage:'
        print '---'
        print 'python run_files  all/neut/fs8[models, datasets] [wini,wwq,wrun,wdist]'
        print 'i.e.'
        print 'python run_files LCDM,wCDM,OkCDM PLK,PLK+DR12'
        print ''
        print 'wini= ini files, wwq= wq files'
        print 'wrun= submit job on the cluster, wdist= dist params'
        print '---'


class Tasks:
    def __init__(self, model, dataset, chains_dir):
        self.model = model
        self.dataset = dataset
        self.full_name = self.model + '_' + self.dataset
	self.chains  = chains_dir


    def write_ini(self):
        """Write params.ini files used by CosmoMC to run the chains"""
        with open('INI_' + self.model + '_' + self.dataset + '.ini', 'w') as f:

            f.write('#Root name for files produced \n')
            f.write('file_root= %s_%s \n'%(self.model, self.dataset))

            #Select datasets
            if ('PLK') in self.dataset:
                f.write("""
#Planck 2015, default just include native likelihoods (others require clik)
DEFAULT(batch2/plik_dx11dr2_HM_v18_TTTEEE.ini)
DEFAULT(batch2/lowTEB.ini)
#DEFAULT(batch2/lfensing.ini)  \n\n""")

            if 'BAO12' in self.dataset: f.write('DEFAULT(batch2/DR12_blows8.ini) \n\n')
            if 'DR12'  in self.dataset: f.write('DEFAULT(batch2/DR12.ini) \n\n')
            if 'JLA'   in self.dataset: f.write('DEFAULT(batch2/JLA.ini) \n\n')


            #write main file
            f.write('DEFAULT(DR12_INI.ini) \n\n')
	    f.write('#Folder where files (chains, checkpoints, etc.) are stored \n')
	    f.write('root_dir = %s \n\n'%(self.chains))


            #select parameters to vary
            f.write('param[omegak] = 0 %s \n'%('-0.1 0.1 0.005 0.005' if 'Ok' in self.model else ''))
            f.write('param[w]      = -1 %s \n'%('-2 0 0.05 0.05'      if 'w' in self.model else ''))
            f.write('param[mnu]    = 0.06 %s \n'%('0 2 0.1 0.1'       if 'mnu' in self.model else ''))
            f.write('param[nnu]    = 3.046 %s \n'%('2 6 0.1 0.1'      if 'Neff' in self.model else ''))
            f.write('param[Alens]  = 1 %s \n'%('0 2 0.1 0.1'          if 'Alens' in self.model else ''))
            f.write('param[Afs8]   = 1 %s \n'%('0 2 0.1 0.1'          if ('Afs8' in self.model or 'ABfs8' in self.model) else ''))
            f.write('param[Bfs8]   = 0 %s \n'%('-2 1 0.1 0.1'         if 'ABfs8' in self.model else ''))




    def write_wq(self, N =20, threads =5):
        """Write wq files to run CosmoMC on the BNL cluster"""
        name = self.full_name

        wq_input = """
mode: bycore
N: %i
threads: %i
hostfile: auto
job_name: %s
command: |
     source ~/.bashrc;
     OMP_NUM_THREADS=%%threads%% mpirun -hostfile %%hostfile%% ./cosmomc INI_%s.ini > %slogs/INI_%s.log 2>%slogs/INI_%s.err
        """%(N, threads, name, name, self.chains, name, self.chains, name)
        with open('wq_' + name + '.ini', 'w') as f:
            f.write(wq_input)





    def write_dist(self):
        """Write distparams files to analaze the chains with Getdist"""
        name =  self.full_name
        i = 1

        with open('distparams_' + name + '.ini', 'w') as f:
            f.write('file_root = %s%s \n\n'%(self.chains, name))
            f.write('INCLUDE(distparams.ini) \n\n')

            f.write('plot%i = omegam H0 \n'%(i));        i+=1

            if 'Ok' in self.model:    f.write('plot%i = omegak H0 \n'%(i));    i+=1
            if 'w' in self.model:     f.write('plot%i = w H0 \n'%(i));         i+=1
            if 'mnu' in self.model:   f.write('plot%i = mnu H0 \n'%(i));       i+=1
            if 'Neff' in self.model:  f.write('plot%i = nnu H0 \n'%(i));       i+=1
            if 'Alens' in self.model: f.write('plot%i = Alens H0 \n\n'%(i));     i+=1

            if self.dataset == 'PLK':
                f.write('compare_num = 3 \n')
                f.write('compare1 = %s_PLK+DR12 \n'%(self.model))
                f.write('compare2 = %s_PLK+DR12+JLA \n'%(self.model))
                f.write('compare3 = Alens_%s_PLK+BAO12 \n'%(self.model))
            else:
                f.write('compare_num = 0 \n')




if __name__ == "__main__":
    TD = To_do('LCDM', 'PLK+BAO12')
    TD.write_ini()
