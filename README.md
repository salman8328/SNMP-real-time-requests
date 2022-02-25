# SNMP-real-time-requests

################################################
this script needs the following inputs:
<Agent IP:port:community> <sample frequency> <number of samples> <OID1> <OID2> …….. <OIDn>
  
this script can be invoked in linux environment with the following command:
<path where this prober.py file is stored>/prober.py <Agent IP:port:community> <sample frequency> <samples> <OID1> <OID2> …….. <OIDn>
  
example of command:
./prober.py 123.21.23.2:public 10 100 1.2.3.21.3654.12 23.032.2.223.335.323
  
########################################################
  
This script works with session API.
  
this code will follow sampling frequency and counter overdlow problems, even when anomolies like SNMP agent restart or counter overflow or SNMP agent response timed out or SNMP agent replied beyond the sampling period.
  
This script will handle all of the problems above !
