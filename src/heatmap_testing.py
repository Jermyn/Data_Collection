import numpy as np
import csv
import pandas
import matplotlib.pyplot as plt
from PIL import Image as im


# data = np.loadtxt(fname='heatmap.csv', delimiter=',')

data = []
# %matplotlib inline

with open('heatmap.csv','rU') as csvfile:
	next(csvfile)
	plots = csv.reader(csvfile, delimiter=',')
	for row in plots:
		if row[12] == '':
			break
		data.append(row[12])

data = np.array(data)	
plt.imshow(im.reshape(im.shape[0], im.shape[1], cmap=plt.cm.Greys))
plt.show()
# print data	