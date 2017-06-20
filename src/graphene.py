import urllib3
import json
import time, threading

axisList = []
axisList_lng = []
count = 0
devList = ['100', '101', '102', '103', '104', '105', '106', '107',
 			'107', '108', '109', '110', '111', '112', '113', '114',
 				'115', '116', '117', '118', '119', '120', '121', '122',
 					'123', '124', '125', '126', '127']
current = open('latest.csv', 'w')
current.write("Device, lat, lng\n")

# def stopwatch(seconds):
# 		start = time.time()
# 		time.clock()
# 		elapsed = 0
# 		while elapsed<seconds:
# 			elapsed=time.time()-start
# 			print "loop cycle time: %f, seconds count: %02d" %(time.clock(), elapsed)
# 			time.sleep(1)

def foo(beaconID, counter):
	global count
	global axisList
	
	
	# start = time.time()
	# time.clock()
	# elapsed = 0
	# while elapsed<seconds:
	# for index in range(0, len(devList)):
	# 	for count in range(0, 10):
			# elapsed=time.time()-start
	http = urllib3.PoolManager()
	r = http.request('GET', 'http://137.132.165.139/api/devices')
	data = json.loads(r.data.decode('utf-8'))[beaconID]['lat']
	data_lng = json.loads(r.data.decode('utf-8'))[beaconID]['lng']
	


	axisList.append(data)
	axisList.append(data_lng)
		# print "loop cycle time: %f, seconds count: %02d" %(time.clock(), elapsed)
		# time.sleep(1)
	
	for i in range(0, len(axisList)):
		 	# current.write(devList[j] + " ")
		 	if i%2==0:
		 		current.write(beaconID + ", " + axisList[i] + ", ")	
		 	else:
		 		current.write(axisList[i] + "\n")
	axisList = []	 			

	return data	 		
	# for j in range(0, 2):
	
exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print "Starting " + self.name
        threadLock.acquire()
        print_time(self.name, self.counter, 5)
        threadLock.release()
        print "Exiting " + self.name  
      

def print_time(threadName, delay, counter):
	index = 0
	while counter:
	    # if exitFlag:
	    #     threadName.exit()
	    time.sleep(delay)
	    # threadLock.acquire()
	    data = foo(threadName, counter)
	    # threadLock.release()
	    print "%s: %s" % (threadName, time.ctime(time.time()) + ", " + data)
	    counter -= 1
	    

threadLock = threading.Lock()
threads = []	    

# Create new threads
thread1 = myThread(100, '100', 1)
thread2 = myThread(101, '101', 1)
thread3 = myThread(102, '102', 1)
thread4 = myThread(103, '103', 1)
thread5 = myThread(104, '104', 1)
thread6 = myThread(105, '105', 1)
thread7 = myThread(106, '106', 1)
thread8 = myThread(107, '107', 1)
thread9 = myThread(108, '108', 1)
thread10 = myThread(109, '109', 1)
thread11 = myThread(110, '110', 1)
thread12 = myThread(111, '111', 1)
thread13 = myThread(112, '112', 1)
thread14 = myThread(113, '113', 1)
thread15 = myThread(114, '114', 1)
thread16 = myThread(115, '115', 1)
thread17 = myThread(116, '116', 1)
thread18 = myThread(117, '117', 1)
thread19 = myThread(118, '118', 1)
thread20 = myThread(119, '119', 1)
thread21 = myThread(120, '120', 1)
thread22 = myThread(121, '121', 1)
thread23 = myThread(122, '122', 1)
thread24 = myThread(123, '123', 1)
thread25 = myThread(124, '124', 1)
thread26 = myThread(125, '125', 1)
thread27 = myThread(126, '126', 1)
thread28 = myThread(127, '127', 1)


# Start new Threads
thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()
thread6.start()
thread7.start()
thread8.start()
thread9.start()
thread10.start()
thread11.start()
thread12.start()
thread13.start()
thread14.start()
thread15.start()
thread16.start()
thread17.start()
thread18.start()
thread19.start()
thread20.start()
thread21.start()
thread22.start()
thread23.start()
thread24.start()
thread25.start()
thread26.start()
thread27.start()
thread28.start()

threads.append(thread1)
threads.append(thread2)
threads.append(thread3)
threads.append(thread4)
threads.append(thread5)
threads.append(thread6)
threads.append(thread7)
threads.append(thread8)
threads.append(thread9)
threads.append(thread10)
threads.append(thread11)
threads.append(thread12)
threads.append(thread13)
threads.append(thread14)
threads.append(thread15)
threads.append(thread16)
threads.append(thread17)
threads.append(thread18)
threads.append(thread19)
threads.append(thread20)
threads.append(thread21)
threads.append(thread22)
threads.append(thread23)
threads.append(thread24)
threads.append(thread25)
threads.append(thread26)
threads.append(thread27)
threads.append(thread28)

for t in threads:
	t.join()
print "Exiting Main Thread"


# stopwatch(20)			


		# print axisList
		# t = threading.Timer(1, foo)
		# t.start()
		# count+=1
		# print repr(count) + "\n"
		# if count == 0:
		# 	for i in range(0, len(axisList)):
		# 	current.write(devList[j] + " ")
		# 		current.write(axisList[i] + " ")

		# 		if i==len(axisList):
		# 			current.write(axisList[i] + "\n")
		# 	axisList = []		
		# 	count = 0
		# 	print "Reset"
			# t.cancel()

	
# for j in range(0, 2):


	# print "Completed\n"

# for i in range(0, len(axisList)):
# 	print axisList[i]