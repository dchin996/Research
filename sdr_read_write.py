import threading
from collections import deque
from threading import Thread
from Queue import Queue
from rtlsdr import *
import matplotlib.pyplot as plt
import numpy as np

# python doesn't have a linked list, so I made my own
class Buffer_Node():

	# each node has a data field (for the deque)
	# next field
	data = None
	next = None

	def __init__ (self):
		pass

	def is_empty(self):
		return self.data == None

data_buffer = Buffer_Node()
write_pointer = data_buffer # pointers in the circular linked list
read_pointer = data_buffer # ''
front = data_buffer
done = False
t_prev = 0

delay = True


def main():
	global data_buffer, front
	constructor_pointer = data_buffer

	# initializes linked list
	for i in range(999): # total of 1000
		constructor_pointer.next = Buffer_Node()
		constructor_pointer = constructor_pointer.next
	constructor_pointer.next = front # to make the linked list circular
	

def write():
	
	sdr = RtlSdr()
	sdr.rs = 1.024e6 # sampling rate
	sdr.fc = 1e6 # center freq

	global write_pointer, done, delay
	i = 0
	while (True):
	#for i in range(100):
		if (i == 2):
			delay = False
		write_window = (sdr_read_samples(Num_of_samples=256*13, sdr_object = sdr))
		# change Num_of_samples to what ever you like per window
		if (write_pointer.data == None):
			write_pointer.data = write_window
		else:
			break
		write_pointer = write_pointer.next
		i += 1
	print ('ERROR')
	print (i) # prints number writing windows created before the ERROR
	done = True
	

def read():
	
	global read_pointer, done, t_prev
	plt.figure()
	plt.title('Amplitude')
	plt.xlabel('time (ms)')
	plt.ylabel('amplitude')
	#plt.show()
	while not(done):
		# if for some reason reading is faster than writing, then wait
		while (read_pointer.data == None):
			
			print("nothing to read")
		time = read_pointer.data[1]
		sample = np.absolute(read_pointer.data[0])
		plt.plot((np.arange(0.0 + t_prev, time + t_prev, time/(len(sample)))), sample)
		# read_pointer.data[0] # array of values
		t_prev += time
		read_pointer.data = None
		read_pointer = read_pointer.next
	# done writing, so just read the rest of the values.
	if (done):
		while not(read_pointer.data == None):
			time = read_pointer.data[1]
			sample = np.absolute(read_pointer.data[0])
			plt.plot((np.arange(0.0 + t_prev, time + t_prev, time/(len(sample)))), sample)
			t_prev += time
			read_pointer.data = None
			read_pointer = read_pointer.next
	# display the graph
	plt.show()

# From sdr.py
def sdr_read_samples(Num_of_samples, sdr_object):
	samples = sdr_object.read_samples(Num_of_samples)
	# measure time in ms
	time = (Num_of_samples/sdr_object.rs)*1000
	return(samples, time)


if __name__ == '__main__':
	global delay
	main()
	
	print ('done initializing')

	Thread(target = write).start() # start writing thread first
	while(delay):
		pass
	Thread(target = read).start() # start reading thread
	