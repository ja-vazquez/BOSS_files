

import pandas as pd

dir  = 'table/'
table = 1
file_output = dir + 'CosmologicalParameters{}.tex'.format(table)


if table == 1:
    models  = ['LCDM', 'OkLCDM', 'woCDM', 'OkwoCDM', 'wowaCDM', 'OkwowaCDM']
    datas   = ['PLK', 'PLK+JLA', 'PLK+BAO12+ALLB', 'PLK+DR12+ALLB', 'PLK+DR12+ALLB+JLA']
    params  = ['Omh2', 'Om', 'H0', 'Ok', 'w', 'wa']
    colsize = (1.8, 3.3, 1.6, 1.5, 1.6, 1.9, 1.6, 1.6)    #In centimeters
    decimal = (4, 3, 1, 4, 2, 2)                         #decimal points

elif table == 2:
    models  = ['mnu', 'mnu_Alens', 'mnu_Afs8', 'mnu_Alens_Afs8',
              #'Neff', 'Neff_Alens', 'Neff_Afs8', 'Neff_Alens_Afs8', 'Neff_mnu', 'Neff_mnu',
               'LCDM_Afs8','LCDM_ABfs8']
    datas   = ['PLK+DR12+ALLB']
    params  = ['H0', 'mnu', 'Alens', 'Afs8', 'ABfs8', 'sigma8']
    colsize = (3.3, 2.5, 1.6, 1.5, 1.5, 1.5, 1.5, 1.5)
    decimal = (1, 2, 2, 2, 2, 2)

else:
    models  = ['Neff', 'OkwoCDM+Neff']
    datas   = ['PLK', 'PLK+DR12+ALLB', 'PLK+DR12+ALLB+HST', 'PLK+DR12+ALLB+JLA', 'PLK+DR12+ALLB+JLA+HST']
    params  = ['Omh2', 'Om', 'H0', 'Ok', 'w', 'Neff']
    colsize = (2., 3.6, 1.6, 1.6, 1.6, 1.6, 1.6, 1.6 )
    decimal = [4, 3, 1, 4, 2, 2]




#--- Latex parameters otherwise raw names---------------------------------------------

assert len(params) is (len(colsize)-2)
assert len(params) is len(decimal)

params_getdist = {'Omh2':'omegamh2*', 'Om':'omegam*', 'H0': 'H0*', 'Ok':'omegak',
                  'w':'w', 'wa':'wa', 'Neff':'nnu', 'mnu':'mnu', 'Alens':'Alens',
                  'Afs8':'Afs8', 'ABfs8':'Bfs8', 'sigma8':'sigma8*'}

params_latex = {'Omh2':'$\Omega_{\\rm m} h^{2}$', 'Om':'$\Omega_{\\rm m}$',
                'H0':'$H_0$', 'Ok':'$\Omega_{\\rm K}$', 'w':'$w_0$', 'wa':'$w_a$',
                'Neff':'$N_{\\rm eff}$', 'mnu':'$\sum m_{\\nu}$ [eV]', 'sigma8':'$\\sigma_8$',
                'Alens':'$A_L$', 'Afs8':'$A_{f\sigma_8}$', 'ABfs8':'$B_{f\sigma_8}$'}

latex_names  = {'LCDM':'$\\Lambda$CDM', 'OkLCDM':'$o$CDM', 'woCDM':'$w$CDM',
                'wowaCDM':'$w_0w_a$CDM', 'HST':'$H_0$',
                'OkwoCDM':'$ow$CDM', 'OkwowaCDM':'$ow_0w_a$CDM',
                'PLK':'Planck', 'DR12':'BAO12 + FS', 'ALLB':'BAO + FS', 'JLA':'SN','BAO12':'BAO',
                'mnu':'$m_{\\nu}$', 'Neff':'$N_{\\rm eff}$',
                'Alens':'$A_L$', 'Afs8':'$A_{f\sigma_8}$', 'ABfs8':'$A_{f\sigma_8}$ + $B_{f\sigma_8}$'}


#--- Code ----------------------------------------------------------------------

def convert_to_latex(model, sep):
    """some names require latex convention"""

    models = dict(enumerate(model.split(sep)))
    full_name = []

    for name in models.values():
        try:
            lname = latex_names[name]
        except:
            lname = name
        full_name.append(lname)
    return " + ".join(full_name)



def main_table(model, data):
    """write its mean/sddev for params in each model"""
    full_line = []
    if not 'CDM' in model: model='LCDM_'+ model
    if 'DR12' in data and 'ALLB' in data: data = data.replace('DR12+', '')
    if 'BAO12' in data and 'ALLB' in data: data = data.replace('+ALLB', '')

    if 'OkwoCDM+Neff' in model: model=model.replace('+','_')

    full_line.append(convert_to_latex(model, sep ='_'))
    full_line.append(convert_to_latex(data, sep ='+'))

    for i, k in enumerate(params):
        try:
            tmp = '%.' + '%if'%(decimal[i])
            if 'mnu' in k:
                full_line.append('$<$ %1.2f'%(float(stats.ix[params_getdist[k]]['upper2'])))
            else:
                mean_values = tmp%(float(stats.ix[params_getdist[k]]['mean']))

                sigma_tmp= float(stats.ix[params_getdist[k]]['sddev'])
                sigma_values = round(sigma_tmp, decimal[i])*10**(decimal[i])

                full_line.append('$%s\ (%i)$'%(mean_values, sigma_values))
        except:
            full_line.append('...')

    return full_line



    #Open Latex Table
outputfile = file(file_output,'w')
outputfile.write(r"\begin{table*}"                                          +'\n')
outputfile.write(r"\centering"                                              +'\n')
outputfile.write(r"\begin{tabular}{%s}"%('p{%fcm}'*len(colsize))%(colsize)  +'\n')
outputfile.write(r"\hline"+'\n')



    #Table headings
pnames, amps = [], []
for i, k in enumerate(params):
     pnames.append(params_latex[k])
     if   'H0'  in k: amps.append('km/s/Mpc')
     elif 'mnu' in k: amps.append(('95\\% limit'))
     else:            amps.append('')

outputfile.write(r"Cosmological  & Data Sets & %s \\"%("&".join(pnames))     +'\n')
outputfile.write(r"Model         &           & %s \\"%("&".join(amps))       +'\n')
outputfile.write(r"\hline"                                                   +'\n')



file_names = ['parameter', 'mean', 'sddev', 'lower1', 'upper1', 'limit1', 'lower2',
              'upper2', 'limit2', 'lower3', 'upper3', 'limit3', 'latex']
i =0
for model in models:
    for data in datas:
        name =  dir + model + '_' + data + '.margestats'
        try:
            stats = pd.read_table(name, skiprows = [0,1], sep='\s+', index_col = 0,
                      names= file_names)
            full_line = main_table(model, data)
            outputfile.write(r"%s                     \\"%("&".join(full_line))  +'\n')
            if (table == 2):
             i+=1
             if i == 4 or i == 6:
                outputfile.write(r"\hline"                                               +'\n')
        except:
            pass
    if (table != 2):outputfile.write(r"\hline"                                               +'\n')
#outputfile.write(r"\hline"                                               +'\n')



    #Closing table
outputfile.write(r"\hline"                                                   +'\n')
outputfile.write(r"\end{tabular}"                                            +'\n')
#outputfile.write(r"\caption{Cosmological constraints.}"                      +'\n')
#outputfile.write(r"\label{tab:DR12}"                                         +'\n')
#outputfile.write(r"\end{table*}"                                             +'\n')
