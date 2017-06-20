import matplotlib.pyplot as plt
import numpy as np

#here's our data to plot, all normal Python lists
x = [1, 2, 3, 4, 5, 6, 7]
y = [1, 2, 3, 4]

intensity = [
    [5, 10, 15, 20, 25, 25, 25],
    [30, 35, 40, 45, 50, 50, 50],
    [55, 60, 65, 70, 75, 75, 75],
    [80, 85, 90, 95, 100, 100, 100]
]

#setup the 2D grid with Numpy
x, y = np.meshgrid(x, y)

#convert intensity (list of lists) to a numpy array for plotting
intensity = np.array(intensity)

#now just plug the data into pcolormesh, it's that easy!
plt.pcolormesh(x, y, intensity)
plt.colorbar() #need a colorbar to show the intensity scale
plt.show() #boom

# import numpy as np 
# from pandas import DataFrame
# import matplotlib.pyplot as plt

# Index= ['aaa', 'bbb', 'ccc', 'ddd', 'eee']
# Cols = ['A', 'B', 'C', 'D']
# df = DataFrame(abs(np.random.randn(5, 4)), index=Index, columns=Cols)

# plt.pcolor(df)
# plt.yticks(np.arange(0.5, len(df.index), 1), df.index)
# plt.xticks(np.arange(0.5, len(df.columns), 1), df.columns)
# plt.show()