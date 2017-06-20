import matplotlib.pyplot as plt
import numpy

plt.close('all')

fake_img = numpy.random.random((10,10))

plt.imshow(fake_img, interpolation='none')
ax  = plt.gca()
fig = plt.gcf()

linepoints = numpy.array([])

def onclick(event):
    if event.button == 3:
        global linepoints

        x = event.xdata
        y = event.ydata

        linepoints = numpy.append(linepoints, x)
        linepoints = numpy.append(linepoints, y)

        if numpy.size(linepoints) == 4:
            plt.plot((linepoints[0], linepoints[2]), (linepoints[1], linepoints[3]), '-')
            linepoints = numpy.array([])
            plt.show()

cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()