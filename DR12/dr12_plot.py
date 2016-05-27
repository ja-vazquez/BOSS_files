
from getdist import plots


dir_name = '/Users/josevazquezgonzalez/Desktop/BOSS/BOSS_files/DR12/chains'

roots = ['owcdmdr12','OkwoCDM_PLK+BAO12','OkwoCDM_PLK+DR12']
g = plots.getSubplotPlotter(chain_dir= dir_name, width_inch=16, analysis_settings={'smooth_scale_2D': -1.})
g.settings.axes_fontsize = 18
g.settings.lab_fontsize = 20
g.settings.alpha_filled_add =0.9

g.plots_2d(roots, param_pairs=[['omegak','w'], ['omegak','H0'], ['w','H0']], nx=3, filled=True,
           legend_labels=False, line_args={'lw':2,  'ls':'-'})

g.add_legend(['PLACK + DR12 LOWZ+CMASS', 'PLACK + DR12 BAO', 'PLACK + DR12 BAO+RSD'],
             colored_text=True,  legend_loc='upper right')
g.export('comp_lowz.pdf')


roots = ['OkwowaCDM_PLK+BAO12','OkwowaCDM_PLK+DR12', 'OkwowaCDM_PLK+DR12+JLA']

g = plots.getSubplotPlotter(chain_dir= dir_name, width_inch=16,  analysis_settings={'smooth_scale_2D': -1.})
g.settings.axes_fontsize = 18
g.settings.lab_fontsize = 20
g.settings.alpha_filled_add =0.9

g.plots_2d(roots, param_pairs=[['omegak','w'], ['omegak','wa'], ['w','wa']], nx=3, filled=True,
           legend_labels=False)
g.add_legend(['PLACK + DR12 LOWZ+CMASS', 'PLACK + DR12 BAO', 'PLACK + DR12 BAO+RSD'],
             colored_text=True,  legend_loc='upper right')
g.export('owa_dr12_jla.pdf')



roots = ['LCDM_ABfs8_PLK+DR12']

g = plots.getSinglePlotter(chain_dir= dir_name, analysis_settings={'smooth_scale_2D': -1.})
g.settings.axes_fontsize = 18
g.settings.lab_fontsize = 20
g.settings.alpha_filled_add =0.9
g.add_y_marker(0)
g.add_x_marker(1)
g.plot_2d(roots, 'Afs8','Bfs8', filled=True, legend_labels=False)
g.add_legend(['MG'], colored_text=True,  legend_loc='upper right')
g.export('mg.pdf')




roots = ['mnu_Alens_Afs8_PLK+DR12', 'mnu_Alens_PLK+DR12',  'mnu_Afs8_PLK+DR12', 'mnu_PLK+DR12']

g = plots.getSinglePlotter(chain_dir= dir_name, analysis_settings={'smooth_scale_2D': -1.})
g.settings.axes_fontsize = 18
g.settings.lab_fontsize = 20
g.settings.alpha_filled_add =0.9
g.settings.legend_fontsize = 16

g.plot_2d(roots, 'mnu','H0', filled=True, legend_labels=False, lims = [ 0.00, 0.5, 64.9,71])
g.add_legend(['$\sum m_{\\nu}$ + $A_L$ + $A_{f\sigma_8}$',
              ' $\sum m_{\\nu}$ + $A_L$',
                '$\sum m_{\\nu}$ + $A_{f\sigma_8}$',
             '$\sum m_{\\nu}$ '],
             colored_text=True,  legend_loc='upper right')
g.export('mnu.pdf')


roots = ['Neff_Alens_Afs8_PLK+DR12', 'Neff_Alens_PLK+DR12',  'Neff_Afs8_PLK+DR12', 'Neff_PLK+DR12']

g = plots.getSinglePlotter(chain_dir= dir_name, analysis_settings={'smooth_scale_2D': -1.})
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

g= plots.getSinglePlotter(chain_dir = dir_name, ratio=1., analysis_settings={'smooth_scale_2D': -1.})
g.plot_2d(roots, param_pair=['omegak','w'], filled=True, legend_labels=False, line_args={'lw':2,  'ls':'-'})

g.settings.axes_fontsize = 20
g.settings.lab_fontsize = 25
g.settings.alpha_filled_add =0.9
g.add_y_marker(-1)
g.add_x_marker(0)

g.export('OkwoCDM_10.pdf')


roots = ['owcdmdr12','OkwoCDM_PLK+BAO12','OkwoCDM_PLK+DR12']

g= plots.getSinglePlotter(chain_dir = dir_name, ratio=1., analysis_settings={'smooth_scale_2D': -1.})
g.plot_2d(roots, 'omegak','H0', filled=True, legend_labels=False, line_args={'lw':2,  'ls':'-'})

g.settings.axes_fontsize = 20
g.settings.lab_fontsize = 25
g.settings.alpha_filled_add =0.9

g.add_x_marker(0)
g.export('OkwoCDM_2.pdf')


roots = ['owcdmdr12','OkwoCDM_PLK+BAO12','OkwoCDM_PLK+DR12']

g= plots.getSinglePlotter(chain_dir = dir_name, ratio=1., analysis_settings={'smooth_scale_2D': -1.})
g.plot_2d(roots, 'w','H0', filled=True, legend_labels=False, line_args={'lw':2,  'ls':'-'})

g.settings.axes_fontsize = 20
g.settings.lab_fontsize = 25
g.settings.alpha_filled_add =0.9

g.add_x_marker(-1)

g.add_legend(['PLACK + DR12 LOWZ+CMASS', 'PLACK + DR12 BAO', 'PLACK + DR12 BAO+RSD'], 
		             colored_text=True,  legend_loc='upper right')
g.export('OkwoCDM_3.pdf')


roots = ['OkwoCDM_PLK+JLA', 'OkwoCDM_PLK+BAO12', 'OkwoCDM_PLK+DR12', 'OkwoCDM_PLK+DR12+JLA']

g= plots.getSinglePlotter(chain_dir = dir_name, ratio=1., analysis_settings={'smooth_scale_2D': -1.})
g.plot_2d(roots, param_pair=['omegak','w'], filled=True, legend_labels=False, line_args={'lw':2,  'ls':'-'})

#g = plots.getSubplotPlotter(chain_dir= dir_name, width_inch=16, analysis_settings={'smooth_scale_2D': -1.})
g.settings.axes_fontsize = 20
g.settings.lab_fontsize = 25
g.settings.alpha_filled_add =0.9
g.add_y_marker(-1)
g.add_x_marker(0)

#g.plots_2d(roots, param_pairs=[['omegak','w'], ['omegak','H0'], ['w','H0']], nx=3, filled=True,
#           legend_labels=False, line_args={'lw':2,  'ls':'-'})

g.add_legend(['PLANCK+SN', 'PLANCK+BAO', 'PLANCK+BAO+RSD', 'PLANCK+BAO+RSD+SN'],
             colored_text=True,  legend_loc='lower right')
g.export('OkwoCDM_all.pdf')


roots = ['wowaCDM_PLK+JLA','wowaCDM_PLK+BAO12', 'wowaCDM_PLK+DR12', 'wowaCDM_PLK+DR12+JLA']

g= plots.getSinglePlotter(chain_dir = dir_name, ratio=1., analysis_settings={'smooth_scale_2D': -1.})
g.plot_2d(roots, param_pair=['w','wa'], filled=True, legend_labels=False, line_args={'lw':2,  'ls':'-'},
             lims=[-1.8,0,-1.8,1.5])

#g = plots.getSubplotPlotter(chain_dir= dir_name, width_inch=16, analysis_settings={'smooth_scale_2D': -1.})
g.settings.axes_fontsize = 20
g.settings.lab_fontsize = 25
g.settings.alpha_filled_add =0.9
g.add_y_marker(0)
g.add_x_marker(-1)

#g.plots_2d(roots, param_pairs=[['omegak','w'], ['omegak','H0'], ['w','H0']], nx=3, filled=True,
#           legend_labels=False, line_args={'lw':2,  'ls':'-'})

g.add_legend(['PLANCK+SN','PLANCK+BAO', 'PLANCK+BAO+RSD', 'PLANCK+BAO+RSD+SN'],
             colored_text=True,  legend_loc='upper right')
g.export('wowaCDM_all.pdf')


