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

No = "0"
para = read_input.ReadInput('inputfiles/constrained_spheres.dat.' + No)
path = "data/" + No


np.random.seed(int(No))


for sample_iter in range(sample):
    rd_quaternion1 = np.random.rand(4)-0.5
    rd_quaternion1 = list(rd_quaternion1/np.linalg.norm(rd_quaternion1, ord=2))
    rd_quaternion1 = '	'.join(str_list(rd_quaternion1))
    rd_quaternion2 = np.random.rand(4)-0.5
    rd_quaternion2 = list(rd_quaternion2/np.linalg.norm(rd_quaternion2, ord=2))
    rd_quaternion2 = '	'.join(str_list(rd_quaternion2))
    rd_quaternion3 = np.random.rand(4)-0.5
    rd_quaternion3 = list(rd_quaternion3/np.linalg.norm(rd_quaternion3, ord=2))
    rd_quaternion3 = '	'.join(str_list(rd_quaternion3))

    bodies = open(os.path.join(path, "constrained_spheres.clones"), "w")
    d = para.debye_length
    h = str(para.debye_length_wall)
    bodies.write("3\n \
                0	0	" + h + "	" + rd_quaternion1 + "\n" + \
                str(d) +"	0	" + h + "	" + rd_quaternion2 + "\n" + \
                str(d * np.cos(np.pi/2.)) +"	" + str(d * np.sin(np.pi/2.)) + "	" + h + "	" + rd_quaternion3
                )

    sys.argv = ['multi_bodies_utilities.py', '--input-file', 'inputfiles/constrained_spheres.dat.' + No]
    execfile('multi_bodies_utilities.py')

    with open(os.path.join(path, "mob.body_mobility.dat"), 'r') as f:
        head, blob_model = ntpath.split(para.structures[0][0])
        result = open(os.path.join(path, blob_model.split('.')[0] + ".mob." + str(sample_iter)), "w")
        result.write(f.read())
        result.close()























#
