import matplotlib.pyplot as plt
import numpy as np
fileHeader = 'C:/Users/Liam Droog/Downloads'
file = '/s60.Master.sample'
data = np.genfromtxt(fileHeader+file, skip_header=14, skip_footer=1)
plt.plot(data[:,0], data[:,1] / np.linalg.norm(data[:,1]))
plt.show()

