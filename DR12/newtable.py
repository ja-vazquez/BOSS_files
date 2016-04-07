import numpy as np

#outputfile = file('table.dat','w')
#for l in range(221):
#   outputfile.write("%f %f %f %f %f\n" %(xint[l],zint_low2[l],zint_low1[l],zint_upp1[l],zint_upp2[l]))
#outputfile.close()

def value(file,name):

    data=np.loadtxt(file+'.margestats', skiprows=3, comments='#', usecols=[0,1,2],dtype='S')#{'names': ('param', 'avg', 'std'), 'formats': ('S10','f13','f13')})
    par=data[:,0]
    avg=data[:,1].astype(np.float)
    std=data[:,2].astype(np.float)

    for i in range(np.size(par)):
        if(par[i]==name):
            return avg[i],std[i]



def pass_to_latex(model, data_set):
    file = model + '_' + data_set

    omh2_avg,omh2_std = value(file, 'omegamh2*')
    om_avg,  om_std   = value(file, 'omegamh2*')
    h0_avg,  h0_std   = value(file, 'H0*')

    par_1 =  r"%.4f (%i)  "%(omh2_avg,np.rint(10000*omh2_std))
    par_2 =  r"%.3f (%i)  "%(om_avg,np.rint(1000*om_std))
    par_3 =  r"%.1f (%i)  "%(h0_avg,np.rint(10*h0_std))
    par_4 =  r"-"
    par_5 =  r"-"
    par_6 =  r"-\\"

    seq = ( model,data_set,par_1, par_2, par_3, par_4, par_5, par_6 )
    return  "&".join(seq)


#===================================================================




size_col = (2.5, 1.5, 1.5, 1.5, 1.5, 1.5)
models    = ['LCDM']
data_sets = ['PLK+BAO12', 'PLK+DR12']


outputfile = file('table/newtable.tex','w')

outputfile.write(r"\begin{table*}"+'\n')
outputfile.write(r"\centering"+'\n')
outputfile.write(r"\begin{tabular}{P{2.cm}P{5.cm}   P{%fcm} P{%fcm} P{%fcm} P{%fcm} P{%fcm} P{%fcm}}"%(size_col)+'\n')
outputfile.write(r"\hline"+'\n')
outputfile.write(r"Model & Data Sets & $\Omega_{\rm m} h^{2}$ & $\Omega_{\rm m}$ & $H_{0}$ & $\Omega_{\rm K}$ & $w_{0}$ & $w_{a}$ \\"+'\n')
#outputfile.write(r"Model & & & & km s$^{-1}$ Mpc$^{-1}$ & & & \\"+'\n\n')
outputfile.write(r" & & & & & & & \\"+'\n')
outputfile.write(r"\hline"+'\hline\n')


for model in models:
    for data_set in data_sets:
        outputfile.write( pass_to_latex(model, data_set))
    outputfile.write(r" \hline"+'\n')







outputfile.write(r"\end{tabular}"+'\n')
outputfile.write(r"\caption{Cosmological constraints.}"+'\n')
outputfile.write(r"\label{tab:DR12}"+'\n')
outputfile.write(r"\end{table*}"+'\n')

outputfile.close()

