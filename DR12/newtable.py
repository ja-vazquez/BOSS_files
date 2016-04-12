import numpy as np
from collections import defaultdict


dic_name = defaultdict(list)
dic_name['LCDM']   = "$\Lambda$CDM"
dic_name['wCDM']   = "$w$CDM"
dic_name['OkwCDM'] = "$ow$CDM"
dic_name['PLK']    = 'Planck'



def value(file, name, sig_times=1):
    """Read margestats and assign mean and 1std for each parameter"""
    data= np.loadtxt('table/' + file + '.margestats', skiprows=3, comments='#', usecols=[0,1,2], dtype='S')
    par = data[:,0]
    avg = data[:,1].astype(np.float)
    std = data[:,2].astype(np.float)

    for i, pname in enumerate(par):
        if(pname == name):
            return avg[i], np.rint(sig_times*std[i])



def latex_name(model, sep):
    """some names require latex convention"""
    models = dict(enumerate(model.split(sep)))
    full_name = []

    for name in models.values():
        name = dic_name[name] if dic_name[name] else name
        full_name.append(name)
    return " + ".join(full_name)




def pass_to_latex(model, data_set, params):
    """get values and errorbars to be written on the table"""
    file = model + '_' + data_set

        #function value returns:  avg, std*times
    par_Omh2 = r"%.4f (%i)  "%(value(file, 'omegamh2*', sig_times= 10**4 ))
    par_Om   = r"%.3f (%i)  "%(value(file, 'omegam*', 10**3))
    par_H0   = r"%.1f (%i)  "%(value(file, 'H0*',   10**1))
    par_Ok   = r"%.4f (%i) "%(value(file, 'omegak',  10**4)) if 'Ok' in model else r"..."
    par_w    = r"%.2f (%i) "%(value(file, 'w',       10**2)) if 'w' in model  else r"..."
    par_wa   = r"%.2f (%i) "%(value(file, 'wa',       10**2))if 'wa' in model else r"..."
    par_nnu  = r"%.1f (%i) "%(value(file, 'nnu',     10**1)) if 'Neff' in model else r"..."
    par_Alen = r"%.2f (%i) "%(value(file, 'Alens',   10**2)) if 'Alens' in model else r"..."
    par_Afs8 = r"%.2f (%i) "%(value(file, 'Afs8',    10**2)) if 'Afs8' in model else r"..."

    model_name = latex_name(model,    sep ='_')
    data_name  = latex_name(data_set, sep ='+')
    seq = [model_name, data_name]

    for par in params:
        seq.append(eval('par_' +  par))
    full_line = "&".join(seq) + r"\\"

    return  full_line




def set_of_models(models, data_sets, params):
    """write each line of the table"""
    for model in models:
        for data_set in data_sets:
            try:
                outputfile.write(r"%s"%(pass_to_latex(model, data_set, params)))
            except:
                pass
    outputfile.write(r" \hline"+'\n')



#----------------------------------------------------------------------------------------

    #write first lines of Latex
size_col = (2.5, 3., 1.8, 1.8, 2.5, 2., 1.8, 1.8)
outputfile = file('table/newtable.tex','w')

outputfile.write(r"\begin{table*}"+'\n')
outputfile.write(r"\centering"+'\n')
outputfile.write(r"\begin{tabular}{p{%fcm} p{%fcm} p{%fcm} p{%fcm} p{%fcm} "
                 r"p{%fcm} p{%fcm} p{%fcm} }"%(size_col)+'\n')
outputfile.write(r"\hline"+'\n')
outputfile.write(r"Cosmological & Data Sets & $\Omega_{\rm m} h^{2}$ & $\Omega_{\rm m}$ & $H_{0}$ & "
                 r" $\Omega_{\rm K}$ & $w_0$ & $w_a$ \\"+'\n')
outputfile.write(r"Model & & & & km s$^{-1}$ Mpc$^{-1}$ & & & \\"+'\n')
outputfile.write(r" & & & & &  \\"+'\n')
outputfile.write(r"\hline"+'\hline\n')


    #Write table for set of models
#-----------------------------------------------------------------
models    = ['LCDM', 'wCDM', 'OkwCDM']
data_sets = ['PLK+BAO12', 'PLK+DR12']
params = ['Omh2', 'Om', 'H0', 'Ok', 'w', 'nnu']
set_of_models(models, data_sets, params)

    # Close table
outputfile.write(r"\end{tabular}"+'\n')
outputfile.write(r"\caption{Cosmological constraints.}"+'\n')
outputfile.write(r"\label{tab:DR12}"+'\n')
outputfile.write(r"\end{table*}"+'\n')

outputfile.close()











if False:
    #write first lines of Latex
 size_col = (2., 3., 1.8, 1.8, 2.9, 1.9, 1.5, 1.5, 1.5, 1.5)
 outputfile = file('table/newtable2.tex','w')

 outputfile.write(r"\begin{table*}"+'\n')
 outputfile.write(r"\centering"+'\n')
 outputfile.write(r"\begin{tabular}{P{%fcm}P{%fcm}  P{%fcm} P{%fcm} P{%fcm} "
                 r"P{%fcm} P{%fcm} P{%fcm} P{%fcm} P{%fcm}}"%(size_col)+'\n')
 outputfile.write(r"\hline"+'\n')
 outputfile.write(r"Cosmological & Data Sets & $\Omega_{\rm m} h^{2}$ & $\Omega_{\rm m}$ & $H_{0}$ & "
                 r" $\Omega_{\rm K}$ & $w$ & ${\rm Neff}$& ${\rm A_{lens}}$ & ${\rm A_{fs8}}$ \\"+'\n')
 outputfile.write(r"Model & & & & km s$^{-1}$ Mpc$^{-1}$ & & & \\"+'\n')
 outputfile.write(r" & & & & & & & \\"+'\n')
 outputfile.write(r"\hline"+'\hline\n')


    #Write table for set of models
#-----------------------------------------------------------------

 data_sets = ['PLK+DR12']

 models    = ['Neff', 'Neff_Alens', 'Neff_Afs8', 'Neff_Alens_Afs8']
 set_of_models(models, data_sets)

 models    = ['mnu', 'mnu_Alens', 'mnu_Afs8', 'mnu_Alens_Afs8']
 set_of_models(models, data_sets)

 models    = ['LCDM_Afs8', 'LCDM_ABfs8']
 set_of_models(models, data_sets)


    # Close table
 outputfile.write(r"\end{tabular}"+'\n')
 outputfile.write(r"\caption{Cosmological constraints.}"+'\n')
 outputfile.write(r"\label{tab:DR12}"+'\n')
 outputfile.write(r"\end{table*}"+'\n')

 outputfile.close()