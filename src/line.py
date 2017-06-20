import matplotlib.pyplot as plt
import csv
import sys

dev_402 = []
dev_403 = []
dev_404 = []
dev_405 = []
actual = []
x = []
y = []

# def extract_write_file(filename):
with open(sys.argv[-1],'rU') as csvfile:
	next(csvfile)
	plots = csv.reader(csvfile, delimiter=',')
	for row in plots:
		# x.append((row[0]))
		# y.append((row[1]))
		actual.append((row[1]))
 		dev_402.append((row[2]))
 		dev_403.append((row[3]))
 		dev_404.append((row[4]))
 		dev_405.append((row[5])) 
	# print dev_402	   	

# extract_write_file('Lat&Lon.txt')	
# with open('Lat&Lon.txt','r') as csvfile:
# 	#next(csvfile)
# 	plots = csv.reader(csvfile, delimiter=' ')
# 	for row in plots:
# 		# actual.append((row[1]))
# 		# dev_402.append((row[2]))
# 		# dev_403.append((row[3]))
# 		# dev_404.append((row[4]))
# 		# dev_405.append((row[5]))
# 		x.append(row[0])
# 		y.append(row[1])	
# 	print x
# 	print y
plt.plot(actual, label='Actual Values')
if sys.argv[-1] == "lon_data.txt":
	plt.plot(dev_402, label='Measured Longitute for 402')
	plt.plot(dev_403, label='Measured Longitute for 403')
	plt.plot(dev_404, label='Measured Longitute for 404')
	plt.plot(dev_405, label='Measured Longitute for 405')
	plt.xlabel('Longtitude')
# plt.ylabel('Longtitude')
	plt.title('Raw Values of Longtitude\n')
else:
	plt.plot(dev_402, label='Measured Latitute for 402')
	plt.plot(dev_403, label='Measured Latitute for 403')
	plt.plot(dev_404, label='Measured Latitute for 404')
	plt.plot(dev_405, label='Measured Latitute for 405')
	plt.xlabel('Latitude')	
plt.legend()
plt.show()