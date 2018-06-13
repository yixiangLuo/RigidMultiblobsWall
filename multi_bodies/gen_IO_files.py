import sys
import os
import re
import numpy as np

threadsEach = 1
inputFilePath = 'inputfiles/'
outputFilePath = 'data/'

n_steps = 100*1
blob_radius = 0.26201755389999998/2       # 162 blobs
# blob_radius = 0.13505535066599994/2        # 642 blobs
kT = 1
sigma = np.array([0.01])
repulsion_strength = kT/2.0/np.power(sigma, 2)     # quadratic coefficient
# rho = 0.3663/np.sqrt(repulsion_strength)*np.exp(repulsion_strength/kT)       # named "g" in the file
dt = 20/repulsion_strength/1
debye_length = 2.1
repulsion_strength_wall = repulsion_strength
debye_length_wall = 1.1
modelFile = 'Structures/shell_N_162_Rg_0_9497_Rh_1.vertex'
# modelFile = 'Structures/shell_N_642_Rg_0_9767_Rh_1.vertex'

for ex in range(len(repulsion_strength)):
    for thread in range(ex*threadsEach, (ex+1)*threadsEach):
        with open(os.path.join(inputFilePath, "constrained_spheres.dat." + str(thread)), "w") as inputfile:
            inputfile.write('''# Select integrator
scheme                                   stochastic_Slip_Trapz

# Select implementation to compute M and M*f
mobility_blobs_implementation            python
mobility_vector_prod_implementation      pycuda

# Select implementation to compute the blobs-blob interactions
blob_blob_force_implementation           None
body_body_force_torque_implementation    python

# Set time step, number of steps and save frequency
dt                                       ''' + str(dt[ex]) +'''
n_steps                                  ''' + str(n_steps) +'''
n_save                                   1

do_rotation                              False
update_PC                                100

# Set fluid viscosity (eta), gravity (g) and blob radius
eta                                      1.0
g                                        0
blob_radius                              ''' + str(blob_radius) +'''

# Stochastic parameters
kT                                       ''' + str(kT) +'''

# Set parameters for the blob-blob interation
repulsion_strength                       ''' + str(repulsion_strength[ex]) +'''
debye_length                             ''' + str(debye_length) +'''

# Set interaction with the wall
repulsion_strength_wall                  ''' + str(repulsion_strength_wall[ex]) +'''
debye_length_wall                        ''' + str(debye_length_wall) +'''

# seed                                     0

# Set output name
output_name                              data/''' + str(thread) +'''/run

save_clones                              one_file

# Load rigid bodies configuration, provide
# *.vertex and *.clones files
structure ''' + str(modelFile) +''' data/''' + str(thread) +'''/constrained_spheres.clones
            ''')

        if not os.path.exists(outputFilePath + '/' + str(thread)):
            os.makedirs(outputFilePath + '/' + str(thread))
        with open(os.path.join(outputFilePath + '/' + str(thread), "constrained_spheres.clones"), "w") as cloneFile:
            cloneFile.write(' ')





















#
