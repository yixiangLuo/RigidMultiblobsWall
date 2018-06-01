import sys
import os
import re
import numpy as np
sys.path.append('../')
from read_input import read_input
import ntpath

sample = 100

def str_list(l):
    return [str(e) for e in list(l)]

No = "8"
para = read_input.ReadInput('inputfiles/constrained_spheres.' + No + '.dat')
path = "data/" + No


np.random.seed(int(para.seed))


for sample_iter in range(sample):
    rd_quaternion1 = np.random.rand(4)-0.5
    rd_quaternion1 = list(rd_quaternion1/np.linalg.norm(rd_quaternion1, ord=2))
    rd_quaternion1 = '	'.join(str_list(rd_quaternion1))
    rd_quaternion2 = np.random.rand(4)-0.5
    rd_quaternion2 = list(rd_quaternion2/np.linalg.norm(rd_quaternion2, ord=2))
    rd_quaternion2 = '	'.join(str_list(rd_quaternion2))

    bodies = open(os.path.join(path, "constrained_spheres.clones"), "w")
    sigma = np.sqrt(para.kT/(4*para.repulsion_strength*para.g**2))
    d = [para.debye_length + np.random.normal(0, sigma), para.debye_length + np.random.normal(0, sigma)]
    z = str(para.debye_length_wall)
    bodies.write("3\n \
                0	0	" + z + "	1	0	0	0\n" + \
                str(d[0]) +"	0	" + z + "	" + rd_quaternion1 + "\n" + \
                str(d[1] * np.cos(np.pi/2.)) +"	" + str(d[1] * np.sin(np.pi/2.)) + "	" + z + "	" + rd_quaternion2
                )
    bodies.close()

    sys.argv = ['multi_bodies.py', '--input-file', 'inputfiles/constrained_spheres.' + No + '.dat']
    execfile('multi_bodies.py')

    with open(os.path.join(path, "run.constrained_spheres.config"), 'r') as f:
        head, blob_model = ntpath.split(para.structures[0][0])
        result = open(os.path.join(path, blob_model.split('.')[0] + ".config." + str(sample_iter)), "w")
        result.write(f.read())
        result.close()























#
