import sys
import os
import re
import numpy as np
sys.path.append('../')
from read_input import read_input
import ntpath

para_num = 2
sample_per_para = 7

# angle = np.linspace(1.0/3, 1.0, num=para_num)*np.pi
angle = np.linspace(1.0/3, 1.0/3, num=para_num)*np.pi

epsilon = np.linspace(0.1, 0.01, num=para_num)


def str_list(l):
    return [str(e) for e in list(l)]

No = "1"
para = read_input.ReadInput('inputfiles/constrained_spheres.dat.' + No)
path = "data/" + No

np.random.seed(int(No))

for para_iter in range(para_num):
    for sample_iter in range(sample_per_para):
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
        d = 1*2 + epsilon[para_iter]
        h = 1 + epsilon[para_iter]/2.0

        bodies.write("3\n \
                    0	0	" + str(h) + "	" + rd_quaternion1 + "\n" + \
                    str(d) +"	0	" + str(h) + "	" + rd_quaternion2 + "\n" + \
                    str(d * np.cos(angle[para_iter])) +"	" + str(d * np.sin(angle[para_iter])) + "	" + str(h) + "	" + rd_quaternion3
                    )
        '''
        bodies.write("2\n \
                    0	0	" + str(h) + "	" + rd_quaternion1 + "\n" + \
                    str(d) +"	0	" + str(h) + "	" + rd_quaternion2
                    )
        '''
        '''
        bodies.write("1\n \
                    0	0	" + str(h) + "	" + rd_quaternion1
                    )
        '''

        sys.argv = ['multi_bodies_utilities.py', '--input-file', 'inputfiles/constrained_spheres.dat.' + No]
        execfile('multi_bodies_utilities.py')

        with open(os.path.join(path, "mob.body_mobility.dat"), 'r') as f:
            head, blob_model = ntpath.split(para.structures[0][0])
            result = open(os.path.join(path, blob_model.split('.')[0] + ".mob." + str(para_iter*sample_per_para+sample_iter)), "w")
            result.write(f.read())
            result.close()























#
