

import pandas as pd
from collections import defaultdict

model = 'LCDM'
data = 'PLK+DR12'
dir  = 'table/'
name =  dir + model + '_' + data + '.margestats'

stats = pd.read_table(name, skiprows = [0,1], sep='\s+', index_col = 0,
                      names=['parameter', 'mean', 'sddev', 'lower1', 'upper1', 'limit1', 'lower2',
                             'upper2', 'limit2', 'lower3', 'upper3', 'limit3', 'latex'])

dic_name = defaultdict(list)
dic_name['LCDM']   = "$\\Lambda$CDM"


params = ['Omh2', 'Om', 'H0']
colsize = (2.5, 2.5, 1.8, 1.8, 2.8)
dec_point = (4, 3, 1)
file_output = 'table/newtable_test.tex'

params_stats = {'Omh2':'omegamh2*', 'Om':'omegam*', 'H0': 'H0*'}
params_latex = {'Omh2':'$\Omega_{\\rm m} h^{2}$', 'Om':'$\Omega_{\\rm m}$',
          'H0':'$H_0$'}



def latex_name(model, sep):
    """some names require latex convention"""
    models = dict(enumerate(model.split(sep)))
    full_name = []

    for name in models.values():
        name = dic_name[name] if dic_name[name] else name
        full_name.append(name)
    return " + ".join(full_name)




outputfile = file(file_output,'w')
outputfile.write(r"\begin{table*}"                                          +'\n')
outputfile.write(r"\centering"                                              +'\n')
outputfile.write(r"\begin{tabular}{%s}"%('p{%fcm}'*len(colsize))%(colsize)  +'\n')
outputfile.write(r"\hline"+'\n')



pnames, amps, full_line= [], [], []
full_line.append(latex_name(model,sep ='_'))
full_line.append(latex_name(data, sep ='+'))
for i, k in enumerate(params):
     pnames.append(params_latex[k])
     amps.append('km s$^{-1}$ Mpc$^{-1}$' if 'H0' in k else '')

        #significant numbers
     tmp = '%.' + '%if'%(dec_point[i])
     mean_values = tmp%(float(stats.ix[params_stats[k]]['mean']))
     sigma_values= float(stats.ix[params_stats[k]]['sddev'])*10**(dec_point[i])
     full_line.append('%s (%i)'%(mean_values, sigma_values))


outputfile.write(r"Cosmological  & Data Sets & %s \\"%("&".join(pnames))     +'\n')
outputfile.write(r"Model & & %s                   \\"%("&".join(amps))       +'\n')
outputfile.write(r"\hline"                                                   +'\n')
outputfile.write(r"%s                             \\"%("&".join(full_line))  +'\n')
outputfile.write(r"\hline"                                                   +'\n')
outputfile.write(r"\end{tabular}"                                            +'\n')
outputfile.write(r"\caption{Cosmological constraints.}"                      +'\n')
outputfile.write(r"\label{tab:DR12}"                                         +'\n')
outputfile.write(r"\end{table*}"                                             +'\n')

