

import numpy as np
from numpy.linalg import inv

file = 'consensus_all_covtot_dM_Hz_fsig.txt'
file_inv = 'consensus_all_incovtot_dM_Hz_fsig.txt'

m = np.loadtxt(file)


#print m


n = inv(m)
#print n


np.savetxt(file_inv, n)



# In[7]:

#Let's blow the error bars wherever we have s8
data = np.arange(81).reshape((9,9))

blown_s8 = []
for i in range(9):
    for j in range(9):
        if (j == 2 or j==5 or j==8 or i == 2 or i==5 or i==8):
            blown_s8.append(m[i][j]*10000)
        else:
            blown_s8.append(m[i][j])



blown_new = np.array(blown_s8).reshape((9,9))
#print blown_new



blown_inv =inv(blown_new)
#print blown_inv



np.savetxt('consensus_all_incovtot_dM_Hz_fsig_blown.txt', blown_inv)



