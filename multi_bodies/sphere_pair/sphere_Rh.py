import sys
import re
import numpy as np

sample = 20
PI = 3.141592653
S_SHELL = 0.83284136573349932
# AS_RATIO = [0.735, 0.5, 0.3, 0.25]
AS_RATIO = [0.5]
np.random.seed(2)

def str_list(l):
    return [str(e) for e in list(l)]
def float_list(l):
    return [float(e) for e in list(l)]

para_file = open("sphere_Rh.dat", "r")
para_data = para_file.read()
para_file.close()

Rh_str = ''

for ratio_iter in range(len(AS_RATIO)):

    para_file = open("sphere_Rh.dat", "w")
    ratio_para = "# blob_radius_start\n" + \
    "blob_radius                            " + str(S_SHELL*AS_RATIO[ratio_iter]) + \
    "\n# blob_radius_end"
    spec_para = re.sub(r'# blob_radius_start[\s\S]*# blob_radius_end', ratio_para, para_data)
    para_file.write(spec_para)
    para_file.close()

    velo_d = []
    for j in range(sample):
        rd_quaternion = np.random.rand(4)-0.5
        rd_quaternion = list(rd_quaternion/np.linalg.norm(rd_quaternion, ord=2))
        rd_quaternion = '	'.join(str_list(rd_quaternion))

        bodies = open("Structures/sphere_Rh.clones", "w")
        bodies.write("1\n0	0	0	"+rd_quaternion)
        bodies.close()

        sys.argv = ['multi_bodies_utilities.py', '--input-file', 'sphere_Rh.dat']
        execfile('multi_bodies_utilities.py')

        results = open("data/run.mobility.velocity.dat", "r")
        velocity = float_list(results.readline().strip().split('  '))
        results.close()
        velo_d.append(velocity[0])
    velo_d = np.array(velo_d)
    mean_d = np.mean(velo_d)
    Rh = str(1.0/6/PI/1.0/mean_d)
    Rh_str = Rh_str + Rh + "\n"

Rh_file = open("data/sphere_162.Rh.dat", "w")
Rh_file.write(Rh_str)
Rh_file.close()























#
