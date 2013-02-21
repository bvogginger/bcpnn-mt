import numpy as np
import os
import simulation_parameters
import NeuroTools.parameters as NTP
import ResultsCollector
import re

try:
    from mpi4py import MPI
    USE_MPI = True
    comm = MPI.COMM_WORLD
    pc_id, n_proc = comm.rank, comm.size

except:
    USE_MPI = False
    comm = None
    pc_id, n_proc = 0, 1

network_params = simulation_parameters.parameter_storage()  # network_params class containing the simulation parameters
params = network_params.params

RC = ResultsCollector.ResultsCollector(params)


to_match = 'delayScale1'
dir_names = []
for thing in os.listdir('.'):

    m = re.search('LargeScale(.*)%s$' % to_match, thing)
    if m:
        dir_names.append(thing)


#RC.collect_files()
#dir_names = [#'SmallScale_noBlank_AIII_scaleLatency0.02_wsigmax1.00e-01_wsigmav1.00e-01_wee3.50e-02_wei1.00e-01_wie1.50e-01_wii1.00e-02_delayScale5', \
#        'SmallScale_noBlank_AIII_scaleLatency0.02_wsigmax2.00e-01_wsigmav1.00e-01_wee3.50e-02_wei1.00e-01_wie1.50e-01_wii1.00e-02_delayScale5', \
#        'SmallScale_noBlank_AIII_scaleLatency0.02_wsigmax2.00e-01_wsigmav2.00e-01_wee3.50e-02_wei1.00e-01_wie1.50e-01_wii1.00e-02_delayScale5', \
#        'SmallScale_noBlank_AIII_scaleLatency0.05_wsigmax1.00e-01_wsigmav1.00e-01_wee3.50e-02_wei1.00e-01_wie1.50e-01_wii1.00e-02_delayScale5', \
#        'SmallScale_noBlank_AIII_scaleLatency0.05_wsigmax2.00e-01_wsigmav1.00e-01_wee3.50e-02_wei1.00e-01_wie1.50e-01_wii1.00e-02_delayScale5', \
#        'SmallScale_noBlank_AIII_scaleLatency0.05_wsigmax2.00e-01_wsigmav2.00e-01_wee3.50e-02_wei1.00e-01_wie1.50e-01_wii1.00e-02_delayScale5', \
#        'SmallScale_noBlank_AIII_scaleLatency0.10_wsigmax1.00e-01_wsigmav1.00e-01_wee3.50e-02_wei1.00e-01_wie1.50e-01_wii1.00e-02_delayScale5', \
#        'SmallScale_noBlank_AIII_scaleLatency0.10_wsigmax2.00e-01_wsigmav1.00e-01_wee3.50e-02_wei1.00e-01_wie1.50e-01_wii1.00e-02_delayScale5', \
#        'SmallScale_noBlank_AIII_scaleLatency0.10_wsigmax2.00e-01_wsigmav2.00e-01_wee3.50e-02_wei1.00e-01_wie1.50e-01_wii1.00e-02_delayScale5', \
#        'SmallScale_noBlank_AIII_scaleLatency0.20_wsigmax1.00e-01_wsigmav1.00e-01_wee3.50e-02_wei1.00e-01_wie1.50e-01_wii1.00e-02_delayScale5', \
#        'SmallScale_noBlank_AIII_scaleLatency0.20_wsigmax2.00e-01_wsigmav1.00e-01_wee3.50e-02_wei1.00e-01_wie1.50e-01_wii1.00e-02_delayScale5', \
#        'SmallScale_noBlank_AIII_scaleLatency0.20_wsigmax2.00e-01_wsigmav2.00e-01_wee3.50e-02_wei1.00e-01_wie1.50e-01_wii1.00e-02_delayScale5', \
#        'SmallScale_noBlank_AIII_scaleLatency0.30_wsigmax1.00e-01_wsigmav1.00e-01_wee3.50e-02_wei1.00e-01_wie1.50e-01_wii1.00e-02_delayScale5', \
#        'SmallScale_noBlank_AIII_scaleLatency0.30_wsigmax2.00e-01_wsigmav1.00e-01_wee3.50e-02_wei1.00e-01_wie1.50e-01_wii1.00e-02_delayScale5', \
#        'SmallScale_noBlank_AIII_scaleLatency0.30_wsigmax2.00e-01_wsigmav2.00e-01_wee3.50e-02_wei1.00e-01_wie1.50e-01_wii1.00e-02_delayScale5']
dir_names = [
        'LargeScaleModel_AIII_scaleLatency0.10_wsigmax1.00e-01_wsigmav1.00e-01_wee3.00e-02_wei4.00e-02_wie6.00e-02_wii1.00e-02_delayScale1',
        'LargeScaleModel_AIII_scaleLatency0.10_wsigmax1.00e-01_wsigmav5.00e-02_wee3.00e-02_wei4.00e-02_wie6.00e-02_wii1.00e-02_delayScale1',
        'LargeScaleModel_AIII_scaleLatency0.10_wsigmax5.00e-02_wsigmav1.00e-01_wee3.00e-02_wei4.00e-02_wie6.00e-02_wii1.00e-02_delayScale1',
        'LargeScaleModel_AIII_scaleLatency0.10_wsigmax5.00e-02_wsigmav5.00e-02_wee3.00e-02_wei4.00e-02_wie6.00e-02_wii1.00e-02_delayScale1']

print dir_names

RC.set_dirs_to_process(dir_names)
#print "RC.dirs_to_process", RC.dirs_to_process
RC.get_xvdiff_integral()
RC.get_parameter('w_sigma_x')
RC.get_parameter('w_sigma_v')
print 'RC param_space', RC.param_space
RC.plot_param_vs_xvdiff_integral('w_sigma_x')
#RC.get_cgxv()
#RC.plot_cgxv_vs_xvdiff()

