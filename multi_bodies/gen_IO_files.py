import sys
import os
import re
from math import sqrt, exp

start = 20
threadNum = 5
inputFilePath = 'inputfiles/'
outputFilePath = 'data/'

n_steps = 500
blob_radius = 0.26201755389999998/2       # 162 blobs
# blob_radius = 0.13505535066599994/2        # 642 blobs
kT = 1
repulsion_strength = 8.0     # E
rho = 0.3663/sqrt(repulsion_strength)*exp(repulsion_strength/kT)       # named "g" in the file
dt = 20/repulsion_strength/rho**2
debye_length = 2.1
repulsion_strength_wall = repulsion_strength
debye_length_wall = 2.0
modelFile = 'Structures/shell_N_162_Rg_0_9497_Rh_1.vertex'
# modelFile = 'Structures/shell_N_642_Rg_0_9767_Rh_1.vertex'

for thread in range(start, start+threadNum):
    with open(os.path.join(inputFilePath, "constrained_spheres.dat." + str(thread)), "w") as inputfile:
        inputfile.write('''# Select integrator
scheme                                   Fixman

# Select implementation to compute M and M*f
mobility_blobs_implementation            C++
mobility_vector_prod_implementation      C++

# Select implementation to compute the blobs-blob interactions
blob_blob_force_implementation           None
body_body_force_torque_implementation    python

# Set time step, number of steps and save frequency
dt                                       ''' + str(dt) +'''
n_steps                                  ''' + str(n_steps) +'''
n_save                                   1

# Set fluid viscosity (eta), gravity (g) and blob radius
eta                                      1.0
g                                        ''' + str(rho) +'''
blob_radius                              ''' + str(blob_radius) +'''

# Stochastic parameters
kT                                       ''' + str(kT) +'''

# RFD parameters
rf_delta                                 1.0e-6

# Set parameters for the blob-blob interation
repulsion_strength                       ''' + str(repulsion_strength) +'''
debye_length                             ''' + str(debye_length) +'''

# Set interaction with the wall
repulsion_strength_wall                  ''' + str(repulsion_strength_wall) +'''
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
