#!/bin/python3
#change the above path to your required path, and make sure install the libraries when prompted.

# done by SIDDAVATAM SALMANUDDIN AHAMAD
# BTH
# references in github, easysnmp, wikipedia

#import all the required modules

import math
import easysnmp 
import sys, time 
from easysnmp import Session
from easysnmp import snmp_get

#######################################################################
#take command line arguments and manipulate them to get required arguments in the variables.

info = sys.argv[1] 
args = info.split(':')
ip = args[0]
port_value = args[1]
com = args[2]
s_freq = float(sys.argv[2]) 
s_time = 1/s_freq
samples = int(sys.argv[3])

ID = []
sample_1 = []
sample_2 = []
s_time_arr = []

#this gives us when we need to send samples
for i in range(1,samples):
	s_time_arr = i * s_time 

# gets the required OID values
for i in range(4, len(sys.argv)):
	ID.append(sys.argv[i])
ID.insert(0,'1.3.6.1.2.1.1.3.0') #sysuptime oid

#############################################################################################################################
#finds the rate of change of counter values between the 2 successive samples
#############################################################################################################################
def rate():
	global sample_1, sampling_t, sample_no, samples, loop
	snmp_rep=Session(hostname=ip,remote_port=port_value,community=com,version=2,timeout=1,retries=1).get(ID)
	sampled_t = int(snmp_rep[0].value)*0.01  #agent time
	sample_2 = [] # takes in new counter values

	for index in range(1,len(snmp_rep)):
		if snmp_rep[index].value!='NOSUCHOBJECT' and snmp_rep[index].value!='NOSUCHINSTANCE' and snmp_rep[index].value!='INVALID':
			sample_2.append(int(snmp_rep[index].value)) 

			if sample_no!=0 and len(sample_1)>0 :
				counter_diff = sample_2[index-1] - sample_1[index-1]
				time_diff = sampled_t - sampling_t
				ROID = counter_diff/time_diff # as we know rate = counter_change/time_change

				if counter_diff < 0:
					if snmp_rep[index].snmp_type == 'COUNTER32' and time_diff > 0:
						counter_diff = counter_diff + (2**32) # this solves the wrap around condition for 32 bit counter 

						if index == 1:
							print(str(samp_t) + "|" ,end='')
							fasak = round((counter_diff / time_diff))
							print(str(fasak) + "|" ,end='')
						else:
							fasak = round((counter_diff / time_diff))
							print(str(fasak) + "|")

					elif snmp_rep[index].snmp_type =='COUNTER64' and time_diff > 0: # this solves the wrap around condition for 64 bit counter
						counter_diff = counter_diff + (2**64)

						if index == 1:
							print(str(samp_t) + "|" ,end='')
							fasak = round((counter_diff / time_diff))
							print(str(fasak) + "|" ,end='')
						else:
							fasak = round((counter_diff / time_diff))
							print(str(fasak) + "|" ,end='')
				elif time_diff > 0 :
					if index == 1:
						print(str(samp_t) + "|" ,end='')
						fasak = round((counter_diff / time_diff))
						print(str(fasak) + "|" ,end='')
					else:
						fasak = round((counter_diff / time_diff))
						print(str(fasak) + "|" ,end='')
				elif time_diff < 0: #solves the system reboot problem
					if index == 1:
						sample_2 = []
						sample_1 = []
						loop = range(0, samples+1+2)
						print(str(samp_t) + "|" ,end='')
						print("agent restarted"+ "|")
						
					else:
						sample_2 = []
						sample_1 = []
						loop = range(0, samples+1+2)
						print("agent restarted"+ "|")
					break
							
	if sample_no != 0 and len(sample_1)>0:
		print()
	sample_1 = sample_2 # new sample becomes, old sample to calculate rate
	sampling_t = sampled_t

##################################################################################################################
####################################################################################################################
if samples == -1:
	sample_no = 0
	sample_1 = []
	while 1:
		samp_t = (time.time())
		rate()
		rep_t=(time.time())
		sample_no = sample_no +1
		if rep_t-samp_t > s_time: #solves the problem, where the response from agent is received after the sampling period
			
			time.sleep(s_time-abs(s_time - rep_t+samp_t))
		else:
			time.sleep(abs(s_time - rep_t+samp_t)) # finds the actual time it needs to sleep as the program processing takes time, the actual sleep is lower.
							
else:
	sample_1 = []
	loop = range(0,samples+1)
	for sample_no in loop: # as the samples are > 0, sends, requests to agent that many times.
		samp_t = (time.time()) # records when req is sent
		rate()
		rep_t = (time.time()) # records when req is received
		if rep_t-samp_t > s_time: #solves the problem, where the response from agent is received after the sampling period
			
			time.sleep(s_time-abs(s_time - rep_t+samp_t))
		else:
			time.sleep(abs(s_time - rep_t+samp_t)) # finds the actual time it needs to sleep as the program processing takes time, the actual sleep is lower.
							
	

