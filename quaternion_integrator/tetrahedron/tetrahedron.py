''' 
Script to test a tetrahedron near a wall.  The wall is at z = -h, and
the tetrahedron's "top" vertex is fixed at (0, 0, 0).
'''
import sys
sys.path.append('..')
sys.path.append('../..')
import numpy as np
from quaternion import Quaternion
from quaternion_integrator import QuaternionIntegrator
import uniform_analyzer as ua

ETA = 1.0   # Fluid viscosity.
A = 0.01     # Particle Radius.
H = 10.     # Distance to wall.

def tetrahedron_mobility(position):
  '''
  Calculate the mobility, torque -> angular velocity, at position 
  In this case, position is length 1, as there is just 1 quaternion.
  The mobility is equal to R M^-1 R^t where R is 3N x 3 (9 x 3)
  Rx = r cross x
  r is the distance from the fixed vertex of the tetrahedron to
  each other vertex (a length 3N vector).
  M (3N x 3N) is the singular image stokeslet for a point force near a wall, but
  we've replaced the diagonal piece by 1/(6 pi eta a).
  '''
  r_vectors = get_r_vectors(position[0])
  mobility = image_singular_stokeslet(position[0], r_vectors)
  rotation_matrix = calculate_rot_matrix(position[0], r_vectors)
  total_mobility = np.dot(rotation_matrix.T,
                          np.dot(np.linalg.inv(mobility),
                                 rotation_matrix))
  return total_mobility


def image_singular_stokeslet(quaternion, r_vectors):
  ''' Calculate the image system for the singular stokeslet (M above).'''
  mobility = np.array([np.zeros(9) for _ in range(9)])
  # Loop through particle interactions
  for j in range(3):  
    for k in range(3):
      if j != k:  #  do particle interaction
        r_particles = r_vectors[j] - r_vectors[k]
        r_norm = np.linalg.norm(r_particles)
        r_reflect = r_vectors[j] - (r_vectors[k] - 2.*np.array([0., 0., H])
                                       - 2.*r_vectors[k][2])
        r_ref_norm = np.linalg.norm(r_reflect)
        # Loop through components.
        for l in range(3):
          for m in range(3):
            # Two stokeslets, one with negative force at image.
            mobility[j*3 + l][k*3 + m] = (
              (l == m)*1./r_norm + r_particles[l]*r_particles[m]/(r_norm**3) -
              (l == m)*1./r_ref_norm + r_reflect[l]*r_reflect[m]/(r_ref_norm**3))
        # Add Doublet.
        mobility[(j*3):(j*3 + 3), (k*3):(k*3 + 3)] += 2.*H*stokes_doublet(r_reflect)
        # Add Potential Dipole.
        mobility[(j*3):(j*3 + 3), (k*3):(k*3 + 3)] -= H*H*potential_dipole(r_reflect)
      else:
        mobility[(j*3):(j*3 + 3), (k*3):(k*3 + 3)] = 1./(6*np.pi*ETA*A)*np.identity(3)
      
  return mobility
              
def stokes_doublet(r):
  ''' Calculate stokes doublet from direction, strength, and r. '''
  r_norm = np.linalg.norm(r)
  e3 = np.array([0., 0., 1.])
  doublet = (np.outer(r, e3) + np.dot(r, e3)*np.identity(3) -
             np.outer(e3, r) - 3.*np.dot(e3, r)*np.outer(r, r)/(r_norm**2))
  # Negate the first two columns for the correct forcing.
  doublet[:, 0:2] = -1.*doublet[:, 0:2]
  doublet = doublet/(8*np.pi*(r_norm**3))
  return doublet

def potential_dipole(r):
  ''' Calculate potential dipole. '''
  r_norm = np.linalg.norm(r)
  dipole = np.identity(3) - 3.*np.outer(r, r)/(r_norm**2)
  # Negate the first two columns for the correct forcing.
  dipole[:, 0:2] = -1.*dipole[:, 0:2]
  dipole = dipole/(4.*np.pi*(r_norm**3))
  return dipole

  
def calculate_rot_matrix(quaternion, r_vectors):
  ''' Calculate R, 9 by 3 matrix of cross products for r_i. '''
  
  # Create the 9 x 3 matrix.  Each 3x3 block is the matrix for a cross
  # product with one of the r_vectors.
  return np.array([
      #Block 1, cross r_1 
      [0.0, r_vectors[0][2], -1.*r_vectors[0][1]],
      [-1.*r_vectors[0][2], 0.0, r_vectors[0][0]],
      [r_vectors[0][1], -1.*r_vectors[0][0],0.0],
      # Block 2, cross r_2
      [0.0, r_vectors[1][2], -1.*r_vectors[1][1]],
      [-1.*r_vectors[1][2], 0.0, r_vectors[1][0]],
      [r_vectors[1][1], -1.*r_vectors[1][0],0.0],
      # Block 3, cross r_3
      [0.0, r_vectors[2][2], -1.*r_vectors[2][1]],
      [-1.*r_vectors[2][2], 0.0, r_vectors[2][0]],
      [r_vectors[2][1], -1.*r_vectors[2][0],0.0],
      ])


def get_r_vectors(quaternion):
  ''' Calculate r_i from a given quaternion. 
  The initial configuration is hard coded here but can be changed by
  considering an initial quaternion not equal to the identity rotation.
  initial configuration (top down view, the top vertex is fixed at the origin):

                         O r_1 = (0, 2/sqrt(3), -(2 sqrt(2))/3)
                        / \
                       /   \
                      /     \
                     /   O(0, 0, 0)
                    /          \
                   /            \
               -> O--------------O  r_3 = (1, -1/sqrt(3),-(2 sqrt(2))/3)
             /
           r_2 = (-1, -1/sqrt(3),-(2 sqrt(2))/3)

  Each side of the tetrahedron has length 2.
  '''
  initial_r1 = np.array([0., 2./np.sqrt(3.), -2.*np.sqrt(2.)/np.sqrt(3.)])
  initial_r2 = np.array([-1., -1./np.sqrt(3.), -2.*np.sqrt(2.)/np.sqrt(3.)])
  initial_r3 = np.array([1., -1./np.sqrt(3.), -2.*np.sqrt(2.)/np.sqrt(3.)])
  
  rotation_matrix = quaternion.rotation_matrix()

  r1 = np.dot(rotation_matrix, initial_r1)
  r2 = np.dot(rotation_matrix, initial_r2)
  r3 = np.dot(rotation_matrix, initial_r3)
  
  return [r1, r2, r3]

  
def gravity_torque_calculator(position):
  ''' 
  Calculate torque based on position, given as a length
  1 list of quaternions (1 quaternion).  
  '''
  r_vectors = get_r_vectors(position[0])
  R = calculate_rot_matrix(position[0], r_vectors)
  
  # Gravity
  g = np.array([0., 0., -1., 0., 0., -1., 0., 0., -1.])
  return np.dot(R.T, g)


def zero_torque_calculator(position):
  ''' Return 0 torque. '''
  # Gravity
  return np.array([0., 0., 0.])



if __name__ == "__main__":
  # Script to run the fixman integrator on the quaternion.
  initial_position = [Quaternion([1., 0., 0., 0.])]
  fixman_integrator = QuaternionIntegrator(tetrahedron_mobility, 
                                           initial_position, 
                                           zero_torque_calculator)
  # Get command line parameters
  dt = float(sys.argv[1])
  n_steps = int(sys.argv[2])

  uniform_samples = []  
  for k in range(n_steps):
    fixman_integrator.fixman_time_step(dt)
    # Add a uniform sample
    x = np.random.normal(0., 1., 4)
    x = x/np.linalg.norm(x)
    uniform_samples.append(x)

  rotation_analyzer = ua.UniformAnalyzer(fixman_integrator.path, "Fixman")
  samples_analyzer = ua.UniformAnalyzer(uniform_samples, "Samples")

  ua.compare_distributions([rotation_analyzer, samples_analyzer])
  
