import sys
import os
import re
import numpy as np

threadsEach = 1
inputFilePath = 'inputfiles/'
outputFilePath = 'data/'

d = [2.1]

# ----- R_h = 1
# blob_radius = 0.83284136573349932/2       # 12 blobs
# blob_radius = 0.48710611214400001/2       # 42 blobs
# blob_radius = 0.26201755389999998/2       # 162 blobs
# blob_radius = 0.13505535066599994/2        # 642 blobs
# blob_radius = 0.0684099578379999268/2        # 2562 blobs

# modelFile = 'Structures/shell_N_12_Rg_0_7921_Rh_1.vertex'
# modelFile = 'Structures/shell_N_42_Rg_0_8913_Rh_1.vertex'
# modelFile = 'Structures/shell_N_162_Rg_0_9497_Rh_1.vertex'
# modelFile = 'Structures/shell_N_642_Rg_0_9767_Rh_1.vertex'
# modelFile = 'Structures/shell_N_2562_Rg_0_9888_Rh_1.vertex'

# ----- R_g = 1
blob_radius = 1.051462224238267/2       # 12 blobs
# blob_radius = 0.5465330578253432/2       # 42 blobs
# blob_radius = 0.2759044842552673/2       # 162 blobs
# blob_radius = 0.1382831735471675/2        # 642 blobs
# blob_radius = 0.06918299036149883/2        # 2562 blobs

modelFile = 'Structures/shell_N_12_Rg_1_Rh_1_2625.vertex'
# modelFile = 'Structures/shell_N_42_Rg_1_Rh_1_1220.vertex'
# modelFile = 'Structures/shell_N_162_Rg_1_Rh_1_0530.vertex'
# modelFile = 'Structures/shell_N_642_Rg_1_Rh_1_0239.vertex'
# modelFile = 'Structures/shell_N_2562_Rg_1_Rh_1_0113.vertex'

for ex in range(len(d)):
    for thread in range(ex*threadsEach, (ex+1)*threadsEach):
        with open(os.path.join(inputFilePath, "constrained_spheres.dat." + str(thread)), "w") as inputfile:
            inputfile.write('''# Select integrator
scheme                                   body_mobility

# Select implementation to compute M and M*f
mobility_blobs_implementation            C++
mobility_vector_prod_implementation      pycuda

# Select implementation to compute the blobs-blob interactions
blob_blob_force_implementation           None
body_body_force_torque_implementation    python

solver_tolerance                         1.0e-5
rf_delta                                 1.0e-5

# Set fluid viscosity (eta), gravity (g) and blob radius
eta                                      1.0
blob_radius                              ''' + str(blob_radius) +'''

debye_length                             ''' + str(d[ex]) +'''
debye_length_wall                        ''' + str(d[ex]-1) +'''

# Set output name
output_name                              data/''' + str(thread) +'''/mob

# Load rigid bodies configuration, provide
# *.vertex and *.clones files
structure ''' + str(modelFile) +''' data/''' + str(thread) +'''/constrained_spheres.clones
            ''')

        if not os.path.exists(outputFilePath + '/' + str(thread)):
            os.makedirs(outputFilePath + '/' + str(thread))
        with open(os.path.join(outputFilePath + '/' + str(thread), "constrained_spheres.clones"), "w") as cloneFile:
            cloneFile.write(' ')





















#
