
from getdist import plots


dir_name = '/Users/josevazquezgonzalez/Desktop/BOSS/BOSS_files/DR12/chains'


roots = ['owcdmdr12','OkwoCDM_PLK+BAO12','OkwoCDM_PLK+DR12']
g = plots.getSubplotPlotter(chain_dir= dir_name, width_inch=16,
                            analysis_settings={'smooth_scale_2D': -1. , 'ignore_rows': 0.2})
g.settings.axes_fontsize = 18
g.settings.lab_fontsize = 20
g.settings.alpha_filled_add =0.9
g.plots_2d(roots, param_pairs=[['omegak','w'], ['omegak','H0'], ['w','H0']], nx=3, filled=True,
           legend_labels=False, line_args={'lw':2,  'ls':'-'})
g.add_legend(['PLANCK + DR12 LOWZ+CMASS', 'PLANCK + DR12 BAO', 'PLANCK + DR12 BAO+FS'],
             colored_text=True,  legend_loc='upper right')
g.export('comp_lowz.pdf')




roots = ['OkwowaCDM_PLK+BAO12','OkwowaCDM_PLK+DR12', 'OkwowaCDM_PLK+DR12+JLA']
g = plots.getSubplotPlotter(chain_dir= dir_name, width_inch=16,
                            analysis_settings={'smooth_scale_2D': -1. , 'ignore_rows': 0.2})
g.settings.axes_fontsize = 18
g.settings.lab_fontsize = 20
g.settings.alpha_filled_add =0.9
g.plots_2d(roots, param_pairs=[['omegak','w'], ['omegak','wa'], ['w','wa']], nx=3, filled=True,
           legend_labels=False)
g.add_legend(['PLANCK + DR12 LOWZ+CMASS', 'PLANCK + DR12 BAO', 'PLANCK + DR12 BAO+FS'],
             colored_text=True,  legend_loc='upper right')
g.export('owa_dr12_jla.pdf')




roots = ['LCDM_ABfs8_PLK+DR12+ALLB']
g = plots.getSinglePlotter(chain_dir= dir_name,
                           analysis_settings={'smooth_scale_2D': -1., 'ignore_rows': 0.2})
g.settings.axes_fontsize = 20
g.settings.lab_fontsize = 25
g.settings.alpha_filled_add =0.9
g.add_y_marker(0)
g.add_x_marker(1)
g.plot_2d(roots, 'Afs8','Bfs8', filled=True, legend_labels=False, colors = ['blue'], alphas=[0.8])
g.add_legend(['PLANCK+BAO+FS'], colored_text=True,  legend_loc='upper right')
g.export('mg.pdf')



if True:
    roots = ['mnu_Alens_Afs8_PLK+DR12+ALLB', 'mnu_Alens_PLK+DR12+ALLB',  'mnu_Afs8_PLK+DR12+ALLB', 'mnu_PLK+DR12+ALLB']
    g = plots.getSinglePlotter(chain_dir= dir_name,
                               analysis_settings={'smooth_scale_2D': -1. , 'ignore_rows': 0.1})
    g.settings.axes_fontsize = 18
    g.settings.lab_fontsize = 20
    g.settings.alpha_filled_add =0.9
    g.settings.legend_fontsize = 16
    g.plot_2d(roots, 'mnu','H0', filled=True, legend_labels=False, lims = [ 0.00, 0.5, 64.9,71],
              colors = ['green', 'gray', 'red', 'blue'], alphas=[0.8,0.8,0.8,0.8])
    g.add_legend(['$\sum m_{\\nu}$ + $A_L$ + $A_{f\sigma_8}$',
              ' $\sum m_{\\nu}$ + $A_L$',
                '$\sum m_{\\nu}$ + $A_{f\sigma_8}$',
             '$\sum m_{\\nu}$ '],
             colored_text=True,  legend_loc='upper right')
    g.export('mnu_2D.pdf')



roots = ['mnu_Alens_Afs8_PLK+DR12+ALLB', 'mnu_Alens_PLK+DR12+ALLB',  'mnu_Afs8_PLK+DR12+ALLB', 'mnu_PLK+DR12+ALLB']
g = plots.getSinglePlotter(chain_dir= dir_name,
                           analysis_settings={'smooth_scale_1D': -1. , 'ignore_rows': 0.1})
g.settings.axes_fontsize = 20
g.settings.lab_fontsize = 25
g.settings.alpha_filled_add =0.9
g.settings.legend_fontsize = 15
g.settings.legend_frame = False

g.plot_1d(roots, 'mnu', legend_labels=False, colors = ['green', 'gray', 'red', 'blue'])
g.add_legend(['$\sum m_{\\nu}$+$A_L$+$A_{f\sigma_8}$',
              ' $\sum m_{\\nu}$+$A_L$',
                '$\sum m_{\\nu}$+$A_{f\sigma_8}$',
             '$\sum m_{\\nu}$ '],
               legend_loc='upper right')
g.export('mnu.pdf')


if False:
    roots = ['Neff_Alens_Afs8_PLK+DR12', 'Neff_Alens_PLK+DR12',  'Neff_Afs8_PLK+DR12', 'Neff_PLK+DR12']
    g = plots.getSinglePlotter(chain_dir= dir_name,
                               analysis_settings={'smooth_scale_2D': -1. , 'ignore_rows': 0.2})
    g.settings.axes_fontsize = 18
    g.settings.lab_fontsize = 20
    g.settings.alpha_filled_add =0.9
    g.settings.legend_fontsize = 16

    g.plot_2d(roots, 'nnu','H0', filled=True, legend_labels=False)
    g.add_legend(['$N_{eff}$ + $A_L$ + $A_{f\sigma_8}$',
              ' $N_{eff}$+ $A_L$',
                '$N_{eff}$ + $A_{f\sigma_8}$',
             '$N_{eff}$ '],
             colored_text=True,  legend_loc='upper left')
    g.export('Neff.pdf')




roots = ['owcdmdr12','OkwoCDM_PLK+BAO12','OkwoCDM_PLK+DR12']
g= plots.getSinglePlotter(chain_dir = dir_name, ratio=1.,
                          analysis_settings={'smooth_scale_2D': -1., 'ignore_rows': 0.2})
g.plot_2d(roots, param_pair=['omegak','w'], filled=True, legend_labels=False, line_args={'lw':2,  'ls':'-'},
          colors = ['gray', 'red', 'blue'], alphas=[0.8,0.8,0.8])
g.settings.axes_fontsize = 20
g.settings.lab_fontsize = 25
g.settings.alpha_filled_add =0.9
g.add_y_marker(-1)
g.add_x_marker(0)
g.export('OkwoCDM_1.pdf')



roots = ['owcdmdr12','OkwoCDM_PLK+BAO12','OkwoCDM_PLK+DR12']
g= plots.getSinglePlotter(chain_dir = dir_name, ratio=1.,
                          analysis_settings={'smooth_scale_2D': -1. , 'ignore_rows': 0.2})
g.plot_2d(roots, 'omegak','H0', filled=True, legend_labels=False, line_args={'lw':2,  'ls':'-'},
          colors = ['gray', 'red', 'blue'], alphas=[0.8,0.8,0.8])
g.settings.axes_fontsize = 20
g.settings.lab_fontsize = 25
g.settings.alpha_filled_add =0.9
g.add_x_marker(0)
g.export('OkwoCDM_2.pdf')



roots = ['owcdmdr12','OkwoCDM_PLK+BAO12','OkwoCDM_PLK+DR12']
g= plots.getSinglePlotter(chain_dir = dir_name, ratio=1.,
                          analysis_settings={'smooth_scale_2D': -1. , 'ignore_rows': 0.2})
g.plot_2d(roots, 'w','H0', filled=True, legend_labels=False, line_args={'lw':2,  'ls':'-'},
          colors = ['gray', 'red', 'blue'], alphas=[0.8,0.8,0.8])
g.settings.axes_fontsize = 20
g.settings.lab_fontsize = 25
g.settings.alpha_filled_add =0.9
g.add_x_marker(-1)
g.add_legend(['PLANCK + DR12 LOWZ+CMASS', 'PLANCK + DR12 BAO', 'PLANCK + DR12 BAO+FS'],
		             colored_text=True,  legend_loc='upper right')
g.export('OkwoCDM_3.pdf')




roots = ['OkwoCDM_PLK+JLA', 'OkwoCDM_PLK+BAO12', 'OkwoCDM_PLK+DR12', 'OkwoCDM_PLK+DR12+JLA']
g= plots.getSinglePlotter(chain_dir = dir_name, ratio=1.,
                          analysis_settings={'smooth_scale_2D': -1. , 'ignore_rows': 0.2})
g.plot_2d(roots, param_pair=['omegak','w'], filled=True, legend_labels=False, line_args={'lw':2,  'ls':'-'})
g.settings.axes_fontsize = 20
g.settings.lab_fontsize = 25
g.settings.alpha_filled_add =0.9
g.add_y_marker(-1)
g.add_x_marker(0)
g.add_legend(['PLANCK+SN', 'PLANCK+BAO', 'PLANCK+BAO+RSD', 'PLANCK+BAO+FS+SN'],
             colored_text=True,  legend_loc='lower right')
g.export('OkwoCDM_all.pdf')




roots = ['wowaCDM_PLK+JLA','wowaCDM_PLK+BAO12+ALLB', 'wowaCDM_PLK+DR12+ALLB', 'wowaCDM_PLK+DR12+ALLB+JLA']
g= plots.getSinglePlotter(chain_dir = dir_name, ratio=1.,
                          analysis_settings={'smooth_scale_2D': -1. , 'ignore_rows': 0.2})
g.plot_2d(roots, param_pair=['w','wa'], filled=True, legend_labels=False, line_args={'lw':2,  'ls':'-'},
             lims=[-1.8,0,-1.8,1.5], colors = ['green', 'gray', 'red', 'blue'], alphas=[0.8,0.8,0.8,0.8])
g.settings.axes_fontsize = 20
g.settings.lab_fontsize = 25
g.settings.alpha_filled_add =0.9
g.add_y_marker(0)
g.add_x_marker(-1)
g.add_legend(['PLANCK+SN','PLANCK+BAO', 'PLANCK+BAO+RSD', 'PLANCK+BAO+FS+SN'],
             colored_text=True,  legend_loc='upper right')
g.export('wowaCDM_all.pdf')




roots = ['wowaCDM_PLK+JLA','wowaCDM_PLK+BAO12', 'wowaCDM_PLK+DR12', 'wowaCDM_PLK+DR12+JLA']
g= plots.getSinglePlotter(chain_dir = dir_name, ratio=1.,
                          analysis_settings={'smooth_scale_2D': -1. , 'ignore_rows': 0.2})
#g.plot_2d(roots, param_pair=['w','wa'], filled=True, legend_labels=False, line_args={'lw':2,  'ls':'-'},
#             lims=[-1.8,0,-1.9,1.5])


samples = g.sampleAnalyser.samplesForRoot('wowaCDM_PLK+DR12+JLA')
p = samples.getParams()

samples2 = g.sampleAnalyser.samplesForRoot('wowaCDM_PLK+DR12')
p2 = samples2.getParams()

samples3 = g.sampleAnalyser.samplesForRoot('wowaCDM_PLK+BAO12')
p3 = samples3.getParams()

samples4 = g.sampleAnalyser.samplesForRoot('wowaCDM_PLK+JLA')
p4 = samples4.getParams()

ppoint= 0.265905

samples.addDerived( p.w + ppoint*p.wa, name='wz', label='w_p')
samples2.addDerived(p2.w + ppoint*p2.wa, name='wz', label='w_p')
samples3.addDerived(p3.w + ppoint*p3.wa, name='wz', label='w_p')
samples4.addDerived(p4.w + ppoint*p4.wa, name='wz', label='w_p')

samples.updateBaseStatistics()
samples2.updateBaseStatistics()
g.plot_2d(roots, param_pair=['wz','wa'], filled=True,
          legend_labels=False, line_args={'lw':2,  'ls':'-'}, lims=[-1.6,-0.3,-1.9,1.5])
g.settings.axes_fontsize = 20
g.settings.lab_fontsize = 25
g.settings.alpha_filled_add =0.9
g.add_y_marker(0)
g.add_x_marker(-1)
g.add_legend(['PLANCK+SN','PLANCK+BAO', 'PLANCK+BAO+RSD', 'PLANCK+BAO+RSD+SN'], 
		             colored_text=True,  legend_loc='upper right')
g.export('wowaCDM_all_pivot.pdf')



roots = ['Neff_PLK+DR12+ALLB','Neff_PLK+DR12+ALLB+HST']
g= plots.getSinglePlotter(chain_dir = dir_name, ratio=0.8,
                          analysis_settings={'smooth_scale_2D': -1  , 'ignore_rows': 0.2})
g.plot_2d(roots, param_pair=['H0','nnu'], filled=True, legend_labels=False,
        colors = ['blue', 'red', 'OrangeRed'], alphas=[0.9,0.8,0.9,0.9],
          lims=[63, 73, 2, 4])
g.settings.axes_fontsize = 20
g.settings.lab_fontsize = 25
g.add_text('$\Lambda$CDM + $N_{\\rm eff}$', fontsize=22)
g.add_legend([ 'PLANCK+BAO+FS', 'PLANCK+BAO+FS+$H_0$'],
             colored_text=True,  legend_loc='upper left')
g.export('Neff_all.pdf')



roots = ['OkwoCDM+Neff_PLK+DR12+ALLB+JLA', 'OkwoCDM+Neff_PLK+DR12+ALLB+JLA+HST']
g= plots.getSinglePlotter(chain_dir = dir_name, ratio=0.8,
                          analysis_settings={'smooth_scale_2D': -1 , 'ignore_rows': 0.2})
g.plot_2d(roots, param_pair=['H0','nnu'], filled=True, legend_labels=False,
        colors = ['blue', 'red', 'OrangeRed'], alphas=[0.9,0.8,0.9,0.9],
          lims=[63, 73, 2, 4])
g.settings.axes_fontsize = 20
g.settings.lab_fontsize = 25
g.add_text('$ow$CDM + $N_{\\rm eff}$', fontsize=22)
g.add_legend(['PLANCK+BAO+FS+SN', 'PLANCK+BAO+FS+SN+$H_0$'],
             colored_text=True,  legend_loc='upper left')
g.export('Neff_owCDM_all.pdf')