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


outputfile = file('newtable.dat','w')

outputfile.write(r"\begin{table*}"+'\n')
outputfile.write(r"\centering"+'\n')
outputfile.write(r"\begin{tabular}{llllllll}"+'\n')
outputfile.write(r"\hline"+'\n')
outputfile.write(r"Cosmological & Data Sets & $\Omega_{\rm m} h^{2}$ & $\Omega_{\rm m}$ & $H_{0}$ & $\Omega_{\rm K}$ & $w_{0}$ & $w_{a}$ \\"+'\n')
outputfile.write(r"Model & & & & km s$^{-1}$ Mpc$^{-1}$ & & & \\"+'\n')
#outputfile.write(r"Model & & & & & & & \\"+'\n')
outputfile.write(r"\hline"+'\n')


#LCDM
omh2_avg,omh2_std=value('lcdmdr12','omegamh2*')
om_avg,  om_std  =value('lcdmdr12','omegam*')
h0_avg,  h0_std  =value('lcdmdr12','H0*')
outputfile.write(r"$\Lambda$CDM & Planck2015 + LOWZ + CMASS & %.4f (%i) & %.3f (%i) & %.1f (%i) & \nodata & \nodata & \nodata \\" %(omh2_avg,np.int(10000*omh2_std),om_avg,np.int(1000*om_std),h0_avg,np.int(10*h0_std)) +'\n') 
omh2_avg,omh2_std=value('lcdmbaosn','omegamh2*')
om_avg,  om_std  =value('lcdmbaosn','omegam*')
h0_avg,  h0_std  =value('lcdmbaosn','H0*')
outputfile.write(r"$\Lambda$CDM & Planck2015 + BAO + SN & %.4f (%i) & %.3f (%i) & %.1f (%i) & \nodata & \nodata & \nodata \\" %(omh2_avg,np.int(10000*omh2_std),om_avg,np.int(1000*om_std),h0_avg,np.int(10*h0_std)) +'\n')
outputfile.write(r"\hline"+'\n')

#oCDM
omh2_avg,omh2_std=value('ocdmdr12','omegamh2*')
om_avg,  om_std  =value('ocdmdr12','omegam*')
h0_avg,  h0_std  =value('ocdmdr12','H0*')
ok_avg,  ok_std  =value('ocdmdr12','omegak')
outputfile.write(r"oCDM & Planck2015 + LOWZ + CMASS & %.4f (%i) & %.3f (%i) & %.1f (%i) & %+.4f (%i) & \nodata & \nodata \\" %(omh2_avg,np.int(10000*omh2_std),om_avg,np.int(1000*om_std),h0_avg,np.int(10*h0_std),ok_avg,np.int(10000*ok_std)) +'\n') 
omh2_avg,omh2_std=value('ocdmbaosn','omegamh2*')
om_avg,  om_std  =value('ocdmbaosn','omegam*')
h0_avg,  h0_std  =value('ocdmbaosn','H0*')
ok_avg,  ok_std  =value('ocdmbaosn','omegak')
outputfile.write(r"oCDM & Planck2015 + BAO + SN & %.4f (%i) & %.3f (%i) & %.1f (%i) & %+.4f (%i) & \nodata & \nodata \\" %(omh2_avg,np.int(10000*omh2_std),om_avg,np.int(1000*om_std),h0_avg,np.int(10*h0_std),ok_avg,np.int(10000*ok_std)) +'\n')
outputfile.write(r"\hline"+'\n')

#wCDM 
omh2_avg,omh2_std=value('wcdmdr12','omegamh2*')
om_avg,  om_std  =value('wcdmdr12','omegam*')
h0_avg,  h0_std  =value('wcdmdr12','H0*')
w_avg,   w_std   =value('wcdmdr12','w')
outputfile.write(r"$w$CDM & Planck2015 + LOWZ + CMASS & %.4f (%i) & %.3f (%i) & %.1f (%i) & \nodata & %.2f (%i) & \nodata \\" %(omh2_avg,np.int(10000*omh2_std),om_avg,np.int(1000*om_std),h0_avg,np.int(10*h0_std),w_avg,np.int(100*w_std)) +'\n')
omh2_avg,omh2_std=value('wcdmbaosn','omegamh2*')
om_avg,  om_std  =value('wcdmbaosn','omegam*')
h0_avg,  h0_std  =value('wcdmbaosn','H0*')
w_avg,   w_std   =value('wcdmbaosn','w')
outputfile.write(r"$w$CDM & Planck2015 + BAO + SN & %.4f (%i) & %.3f (%i) & %.1f (%i) & \nodata & %.2f (%i) & \nodata \\" %(omh2_avg,np.int(10000*omh2_std),om_avg,np.int(1000*om_std),h0_avg,np.int(10*h0_std),w_avg,np.int(100*w_std)) +'\n')
outputfile.write(r"\hline"+'\n')

#owCDM 
omh2_avg,omh2_std=value('owcdmdr12','omegamh2*')
om_avg,  om_std  =value('owcdmdr12','omegam*')
h0_avg,  h0_std  =value('owcdmdr12','H0*')
ok_avg,  ok_std  =value('owcdmdr12','omegak')
w_avg,   w_std   =value('owcdmdr12','w')
outputfile.write(r"o$w$CDM & Planck2015 + LOWZ + CMASS & %.4f (%i) & %.3f (%i) & %.1f (%i) & %+.4f (%i) & %.2f (%i) & \nodata \\" %(omh2_avg,np.int(10000*omh2_std),om_avg,np.int(1000*om_std),h0_avg,np.int(10*h0_std),ok_avg,np.int(10000*ok_std),w_avg,np.int(100*w_std)) +'\n')
omh2_avg,omh2_std=value('owcdmbaosn','omegamh2*')
om_avg,  om_std  =value('owcdmbaosn','omegam*')
h0_avg,  h0_std  =value('owcdmbaosn','H0*')
ok_avg,  ok_std  =value('owcdmbaosn','omegak')
w_avg,   w_std   =value('owcdmbaosn','w')
outputfile.write(r"o$w$CDM & Planck2015 + BAO + SN & %.4f (%i) & %.3f (%i) & %.1f (%i) & %+.4f (%i) & %.2f (%i) & \nodata \\" %(omh2_avg,np.int(10000*omh2_std),om_avg,np.int(1000*om_std),h0_avg,np.int(10*h0_std),ok_avg,np.int(10000*ok_std),w_avg,np.int(100*w_std)) +'\n')
outputfile.write(r"\hline"+'\n')

#w0waCDM 
omh2_avg,omh2_std=value('w0wacdmdr12','omegamh2*')
om_avg,  om_std  =value('w0wacdmdr12','omegam*')
h0_avg,  h0_std  =value('w0wacdmdr12','H0*')
w_avg,   w_std   =value('w0wacdmdr12','w')
wa_avg,  wa_std  =value('w0wacdmdr12','wa')
outputfile.write(r"$w_0w_a$CDM & Planck2015 + LOWZ + CMASS & %.4f (%i) & %.3f (%i) & %.1f (%i) & \nodata & %.2f (%i) & %.2f (%i) \\" %(omh2_avg,np.int(10000*omh2_std),om_avg,np.int(1000*om_std),h0_avg,np.int(10*h0_std),w_avg,np.int(100*w_std),wa_avg,np.int(100*wa_std)) +'\n')
omh2_avg,omh2_std=value('w0wacdmbaosn','omegamh2*')
om_avg,  om_std  =value('w0wacdmbaosn','omegam*')
h0_avg,  h0_std  =value('w0wacdmbaosn','H0*')
w_avg,   w_std   =value('w0wacdmbaosn','w')
wa_avg,  wa_std  =value('w0wacdmbaosn','wa')
outputfile.write(r"$w_0w_a$CDM & Planck2015 + BAO + SN & %.4f (%i) & %.3f (%i) & %.1f (%i) & \nodata & %.2f (%i) & %.2f (%i) \\" %(omh2_avg,np.int(10000*omh2_std),om_avg,np.int(1000*om_std),h0_avg,np.int(10*h0_std),w_avg,np.int(100*w_std),wa_avg,np.int(100*wa_std)) +'\n')
outputfile.write(r"\hline"+'\n')

#ow0waCDM 
omh2_avg,omh2_std=value('ow0wacdmdr12','omegamh2*')
om_avg,  om_std  =value('ow0wacdmdr12','omegam*')
h0_avg,  h0_std  =value('ow0wacdmdr12','H0*')
ok_avg,  ok_std  =value('ow0wacdmdr12','omegak')
w_avg,   w_std   =value('ow0wacdmdr12','w')
wa_avg,  wa_std  =value('ow0wacdmdr12','wa')
outputfile.write(r"o$w_0w_a$CDM & Planck2015 + LOWZ + CMASS & %.4f (%i) & %.3f (%i) & %.1f (%i) & %+.4f (%i) & %.2f (%i) & %.2f (%i) \\" %(omh2_avg,np.int(10000*omh2_std),om_avg,np.int(1000*om_std),h0_avg,np.int(10*h0_std),ok_avg,np.int(10000*ok_std),w_avg,np.int(100*w_std),wa_avg,np.int(100*wa_std)) +'\n')
omh2_avg,omh2_std=value('ow0wacdmbaosn','omegamh2*')
om_avg,  om_std  =value('ow0wacdmbaosn','omegam*')
h0_avg,  h0_std  =value('ow0wacdmbaosn','H0*')
ok_avg,  ok_std  =value('ow0wacdmbaosn','omegak')
w_avg,   w_std   =value('ow0wacdmbaosn','w')
wa_avg,  wa_std  =value('ow0wacdmbaosn','wa')
outputfile.write(r"o$w_0w_a$CDM & Planck2015 + BAO + SN & %.4f (%i) & %.3f (%i) & %.1f (%i) & %+.4f (%i) & %.2f (%i) & %.2f (%i) \\" %(omh2_avg,np.int(10000*omh2_std),om_avg,np.int(1000*om_std),h0_avg,np.int(10*h0_std),ok_avg,np.int(10000*ok_std),w_avg,np.int(100*w_std),wa_avg,np.int(100*wa_std)) +'\n')
outputfile.write(r"\hline"+'\n')

outputfile.write(r"\end{tabular}"+'\n')
outputfile.write(r"\caption{Cosmological constraints from Planck2015+LOWZ(iso)+CMASS(ani) and from Planck2015+LOWZ(iso)+CMASS(ani)+MGS+6DF+JLA.}"+'\n')
# by different datasets in the cosmological models $\Lambda$CDM, oCDM, $w$CDM, o$w$CDM, $w_0w_a$CDM, and o$w_0w_a$CDM. We compare the cosmological constraints from combining Planck with acoustic scale from BOSS galaxies as well as lower and higher redshift BAO measurements from the 6-degree field galaxy redshift survey (6DF) and the BOSS-Lyman alpha forest (Ly$\alpha$F), respectively. We also compare how these combinations benefit from the constraining power of type-Ia Supernovae from the Union 2 compilation by the Supernovae Cosmology Project (SN). The WMAP and \textit{e}WMAP cases have been added for comparison. As in Table~\ref{tab:bigcos}, 'CMASS-iso' means the isotropic measurement from the CMASS sample, whereas the anisotropic one is referred to simply as 'CMASS'. 'LOWZ' is the isotropic measurement from the LOWZ sample. 'BAO' stands for the combination CMASS + LOWZ + 6DF + Ly$\alpha$F.}"+'\n')
#$H_0$ is in units of km s$^{-1}$ Mpc$^{-1}$.
outputfile.write(r"\label{tab:planck2015}"+'\n')
outputfile.write(r"\end{table*}"+'\n')

outputfile.close()


