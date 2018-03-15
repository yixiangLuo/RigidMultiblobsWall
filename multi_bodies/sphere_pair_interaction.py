import sys
import re
import numpy as np

d_l = 1.0
d_u = 4.0
grid = 20
sample = 20
PI = 3.141592653
S_SHELL = 0.26201755389999998
AS_RATIO = [0.735, 0.5, 0.3, 0.25]
np.random.seed(1)

def str_list(l):
    return [str(e) for e in list(l)]
def float_list(l):
    return [float(e) for e in list(l)]

para_file = open("sphere_pair_interaction.dat", "r")
para_data = para_file.read()
para_file.close()

for ratio_iter in range(len(AS_RATIO)):
    curve = open("data/velocity.ratio-"+ str(AS_RATIO[ratio_iter]) +".curve.dat", "w")
    curve.close()

    para_file = open("sphere_pair_interaction.dat", "w")
    ratio_para = "# blob_radius_start\n" + \
    "blob_radius                            " + str(S_SHELL*AS_RATIO[ratio_iter]) + \
    "\n# blob_radius_end"
    spec_para = re.sub(r'# blob_radius_start[\s\S]*# blob_radius_end', ratio_para, para_data)
    para_file.write(spec_para)
    para_file.close()

    for grid_iter in range(grid):
        velo_d = []
        for j in range(sample):
            rd_quaternion = np.random.rand(4)-0.5
            rd_quaternion = list(rd_quaternion/np.linalg.norm(rd_quaternion, ord=2))
            rd_quaternion = '	'.join(str_list(rd_quaternion))

            bodies = open("Structures/sphere_pair_interaction.clones", "w")
            bodies.write("2\n0	0	1	1	0	0	0\n"+ str(d_l+(d_u-d_l)/grid*grid_iter) +"	0	1	"+rd_quaternion)
            bodies.close()

            sys.argv = ['multi_bodies_utilities.py', '--input-file', 'sphere_pair_interaction.dat']
            execfile('multi_bodies_utilities.py')

            results = open("data/run.mobility.velocity.dat", "r")
            velocity = float_list(results.readline().strip().split('  '))
            results.close()
            velo_d.append(velocity[0]*6*PI*1.0*1.0/1.0)
        velo_d = np.array(velo_d)
        mean_d = str(np.mean(velo_d))
        std_d = str(np.std(velo_d))
        curve = open("data/velocity.ratio-"+ str(AS_RATIO[ratio_iter]) +".curve.dat", "a")
        curve.write(mean_d + " " + std_d + "\n")
        curve.close()























#
