from PIL import Image, ImageDraw
from pylab import *
import matplotlib.pyplot as plt
import matplotlib.image as image
import numpy as np
import csv
import matplotlib.patches as patches
# from bokeh.sampledata.autompg import autompg as df

# print (df)
actual = []
x = []
y = []

def extract_write_file(filename):
	with open(filename,'r') as csvfile:
		next(csvfile)
		plots = csv.reader(csvfile, delimiter=',')
		for row in plots:
			for k in range(0, 3):
				#next(csvfile)
				actual.append((row[k].replace(' ', '')))		
			# x.append((row[0]))
			# y.append((row[1]))    	
extract_write_file('TP_Actual.txt')	

# plt.close('all')



plt.imshow(np.flipud(plt.imread('ActlabImage.png')), origin='lower', extent=[-0.355,0.607,-0.16,0.376], aspect='auto')
show(plt)
# # ax  = plt.gca()
# # fig = plt.gcf()

# # linepoints = np.array([])

# # def onclick(event):
# #     if event.button == 3:
# #         global linepoints

# #         x = event.xdata
# #         y = event.ydata

# #         linepoints = np.append(linepoints, x)
# #         linepoints = np.append(linepoints, y)

# #         if np.size(linepoints) == 4:
# #             plt.plot((linepoints[0], linepoints[2]), (linepoints[1], linepoints[3]), '-')
# #             linepoints = np.array([])
# #             plt.show()

# # cid = fig.canvas.mpl_connect('button_press_event', onclick)

# for i in range(0, len(actual)):
# 	if i%3!=0:
# 		if i%3==1:
# 			y.append(actual[i])
# 		else:	
# 			x.append(actual[i])	
# 
# # # plt.plot((float(x[0]), float(y[0])), (float(x[0]), float(y[0])), '-')
# 
# plt.axis('off')
# plot(x,y, 'r-')
# plot,show()
# # # #ax.add_patch(rect)

# # fig.savefig('Image.png')
# plt.show()

# # read image to array
# # im = array(Image.open('ActlabImage.png'))

# plot the image
# imshow(im.resize(180, 180))

#x = [69.3091,1174.67,1174.67,69.3091]
# y = [143.343, 143.343, 690.073, 690.073]


# # plot the points with red star-markers
# plot(x,y,'r*')
# plot,show()

# im = plt.imshow(np.flipud(plt.imread('ActlabImage.png')), origin='lower',
# 				interpo)

# im = image.imread('ActlabImage.png')
# implot = plt.imshow(im, )
# # draw = ImageDraw.Draw(plt)
# # draw.line((0,0,0.1,0.1), fill=128)
# # ax = plt.subplots(1)
# # locs, labels = plt.xticks()
# # labels = [float(item)*0.5 for item in locs]
# # plt.xticks(locs, labels)

# # tick_locs = [-0.05, 100]
# # tick_labels = [float(item)*5 for item in tick_locs]
# # plt.xticks(tick_locs, tick_labels)

	

# #rect = patches.Rectangle((0,0), 40, 30, linewidth=1, edgecolor='b', facecolor='r')
# # x = [0.5]
# # y = [2.5]
# #fig1 = plt.figure()
# # ax1 = im.add_subplot(111, aspect='equal')
# # fig, ax=plt.subplots(1)
# # ax.add_patch(
# # 	patches.Rectangle(
# # 		(0, 0),
# # 		0.1,
# # 		0.1,
# # 		)
# # 	)
# # fig.show()



# im = np.array(Image.open('ActlabImage.png'), dtype=np.uint8)
# im = plt.imshow(np.flipud(plt.imread('ActlabImage.png')), origin='lower', extent=[-0.355,0.607,-0.16,0.376], aspect='auto')
# Create figure and axes
# fig,ax = plt.subplots(1)

# # Display the image
# ax.imshow(im)

# # Create a Rectangle patch
# rect = patches.Rectangle((-0.26,0.25),0.1,0.1,fill=False)

# # Add the patch to the Axes
# ax.add_patch(rect)

# plt.show()