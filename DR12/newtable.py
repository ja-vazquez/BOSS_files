import numpy as np

#outputfile = file('table.dat','w')
#for l in range(221):
#   outputfile.write("%f %f %f %f %f\n" %(xint[l],zint_low2[l],zint_low1[l],zint_upp1[l],zint_upp2[l]))
#outputfile.close()

def value(file, name, sig_times=1):
     data=np.loadtxt('table/'+file+'.margestats', skiprows=3, comments='#', usecols=[0,1,2],dtype='S')#{'names': ('param', 'avg', 'std'), 'formats': ('S10','f13','f13')})
     par=data[:,0]
     avg=data[:,1].astype(np.float)
     std=data[:,2].astype(np.float)

     for i in range(np.size(par)):
        if(par[i]==name):
            return avg[i],np.rint(sig_times*std[i])




def pass_to_latex(model, data_set):
    file = model + '_' + data_set

    #function value returns:  avg, std*times
    par_1 =  r"%.4f (%i)  "%(value(file, 'omegamh2*', sig_times= 10000 ))
    par_2 =  r"%.3f (%i)  "%(value(file, 'omegam*', 1000))
    par_3 =  r"%.1f (%i)  "%(value(file, 'H0*',       10))
    par_4, par_5, par_6, par_7, par_8  =  r"-", r"-", r"-", r"-", r"-"

    if 'w' in model:
        par_4 =  r"%.2f (%i)  "%(value(file, 'w',       100))
    if 'Ok' in model:
        par_5 =  r"%.2f (%i)  "%(value(file, 'omegak',  10000))
    if 'Neff' in model:
        par_6 = r"%.2f (%i)   "%(value(file, 'nnu',     10))
    if 'Alens' in model:
        par_7 = r"%.2f (%i)   "%(value(file, 'Alens',   10))
    if 'Afs8' in model:
        par_8 = r"%.2f (%i)   "%(value(file, 'Afs8',    10))

    seq = ( model.replace("_","+"),data_set,
            par_1, par_2, par_3, par_4, par_5, par_6,
            par_7, par_8 + r"\\")

    return  "&".join(seq)



def set_of_models(models, data_sets, separation = True):
    for model in models:
        for data_set in data_sets:
            try:
                outputfile.write(r"%s"%(pass_to_latex(model, data_set)))
            except:
                pass
        if separation:
            outputfile.write(r" \hline"+'\n')
    outputfile.write(r" \hline"+'\n')



#----------------------------------------------------------------------------------------

    #write first lines of Latex
size_col = (2.5, 2.5, 1.8, 1.8, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5)
outputfile = file('table/newtable.tex','w')

outputfile.write(r"\begin{table*}"+'\n')
outputfile.write(r"\centering"+'\n')
outputfile.write(r"\begin{tabular}{P{%fcm}P{%fcm}  P{%fcm} P{%fcm} P{%fcm} "
                 r"P{%fcm} P{%fcm} P{%fcm} P{%fcm} P{%fcm}}"%(size_col)+'\n')
outputfile.write(r"\hline"+'\n')
outputfile.write(r"Model & Data Sets & $\Omega_{\rm m} h^{2}$ & $\Omega_{\rm m}$ & $H_{0}$ & "
                 r"$w$ & $\Omega_{\rm K}$ & ${\rm Neff}$& ${\rm A_{lens}}$ & ${\rm A_{fs8}}$ \\"+'\n')
outputfile.write(r" & & & & & & & \\"+'\n')
outputfile.write(r"\hline"+'\hline\n')


    #Write table for set of models
#-----------------------------------------------------------------
models    = ['LCDM', 'wCDM', 'OkwCDM']
data_sets = ['PLK+BAO12', 'PLK+DR12']
set_of_models(models, data_sets)


data_sets = ['PLK+DR12']

models    = ['Neff', 'Neff_Alens', 'Neff_Afs8', 'Neff_Alens_Afs8']
set_of_models(models, data_sets, separation = False)

models    = ['mnu', 'mnu_Alens', 'mnu_Afs8', 'mnu_Alens_Afs8']
set_of_models(models, data_sets, separation = False)

models    = ['LCDM_Afs8', 'LCDM_ABfs8']
set_of_models(models, data_sets, separation = False)


    # Close table
outputfile.write(r"\end{tabular}"+'\n')
outputfile.write(r"\caption{Cosmological constraints.}"+'\n')
outputfile.write(r"\label{tab:DR12}"+'\n')
outputfile.write(r"\end{table*}"+'\n')

outputfile.close()

