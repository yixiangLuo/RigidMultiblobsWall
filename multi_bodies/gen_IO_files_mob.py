import sys
import os
import re
import numpy as np

threadsEach = 1
inputFilePath = 'inputfiles/'
outputFilePath = 'data/'

d = [2.1, 2.066, 2.033, 2.0]

blob_radius = 0.26201755389999998/2       # 162 blobs
# blob_radius = 0.13505535066599994/2        # 642 blobs

modelFile = 'Structures/shell_N_162_Rg_0_9497_Rh_1.vertex'
# modelFile = 'Structures/shell_N_642_Rg_0_9767_Rh_1.vertex'

for ex in range(len(d)):
    for thread in range(ex*threadsEach, (ex+1)*threadsEach):
        with open(os.path.join(inputFilePath, "constrained_spheres.dat." + str(thread)), "w") as inputfile:
            inputfile.write('''# Select integrator
scheme                                   body_mobility

# Select implementation to compute M and M*f
mobility_blobs_implementation            C++
mobility_vector_prod_implementation      C++

# Select implementation to compute the blobs-blob interactions
blob_blob_force_implementation           None
body_body_force_torque_implementation    python

solver_tolerance                         1.0e-3
rf_delta                                 1.0e-3

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
