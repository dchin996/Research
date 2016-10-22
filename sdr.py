# Darin Chin
# 6/30/16
# this program uses the RtlSdr library to recieve signals
# it then uses these values to create a graph using the matplotlib library
# of amplitude over time (ms).


from rtlsdr import * # RtlSdr library
import time
import matplotlib.pyplot as plt
import numpy as np

# Change these as you like.
NUM_BITS = 256*1024 # Number of bits to be read from sdr (minimum is 256)
SAMPLE_RATE = 1.024e6
FREQUENCY = 100e6

# PRE:  Takes in RtlSdr object and sampling array
# POST: Graphs the amplitude over time with given values

def main():
    sdr_read_samples(1024, 125800000, 300e3)

# def graph_amp_over_time(sample_amplitudes, delta):
#     import matplotlib.pyplot as plt
#     import numpy as np

#     plt.figure()
#     print delta/(len(sample_amplitudes))
#     t = np.arange(0.0, delta, delta/(len(sample_amplitudes))) # from zero up to delta with
#                                                              # delta/len(sampleAmplitudes) number of data points
#     s = sample_amplitudes # plot every single amplitude at indexes 0 to (length - 1)
#     plt.plot(t, s)
#     plt.title('Amplitude Over Time')
#     plt.xlabel('time (ms)')
#     plt.ylabel('amplitude')
#     plt.show()

'''
Num_of_samples should be power of 2!
'''
# TODO: change function to get multiplication of sample_rate as Num_of_samples
def sdr_read_samples(Num_of_samples, center_freq, sample_rate):
	# setup RtlSdr object
	sdr = RtlSdr()
	# set rate, freq
	sdr.rs = sample_rate
	sdr.fc = center_freq
	samples = sdr.read_samples(Num_of_samples)
	# measure time in ms
	time = (Num_of_samples/sample_rate)*1000
	return(samples, time)
	
def sdr_time_domain_plot(yData, time):
    plt.figure()
    #print time/len(yData)
    t = np.arange(0.0, time, time/(len(yData))) # from zero up to delta with
                                                             # delta/len(sampleAmplitudes) number of data points
    s = yData
    plt.plot(t, s)
    plt.title('Amplitude')
    plt.xlabel('time (ms)')
    plt.ylabel('amplitude')
    plt.show()
	
'''
read data from binary file with uint8 format
returns samples in iq format
'''
def sdr_read_file(address):
	f = open(address, 'r')
	data = np.fromfile(f, dtype=np.uint8)
	iq_output = (data[0::2]/(255.0/2.0)-1) + (1j*(data[1::2]/(255.0/2.0)-1))
	#iq_output = (data[0::2]) + 1j*(data[1::2])
	f.close()
	return iq_output
		
if __name__ == '__main__':
    main()
