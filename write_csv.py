import sys
import re
import numpy as np
import pandas as pd
import scipy.stats as stats
import sklearn

#probably use numpy or scientific python to do linear regression

counters = {}  #key = counter, val = counter value
power_vals = {} #key = time, val = power value
counter_time = {} #key = time, val = list of counters
time = 2292000000
use_curr_power = 0
inc_t = 1000000000

fpower = open('/home/david/huawei/mul/test2/power_values.out', 'r')
#parse and regularlize the power values
print "Reading Power File"
for line in fpower:
    #have some internal number every 1000ns or something, compare the value in the file with that
    #if file value >= or equal internal value, append value to either list or hash table
    #problem: if file value > internal value, we should technically use the previous lines value (could save 
    #the old line value (prevLine = line), or rather the old time value, not line
    #if the line is time value
    #reg = re.match(r'2  (.{1}\..{7})',line)
    reg1 = re.match(r'2  (.*)',line)
    if (reg1 != None):
        power = reg1.group(1)
        if (use_curr_power):
            power_vals[time] = power
            use_curr_power = 0
            time += inc_t
    else:
        reg = re.match(r'([0-9]{10,11})',line)
        if (reg != None):
            #if file value is equal to time, then we want to use the power value on the line after
            if (int(reg.group(1)) == time):
                use_curr_power = 1;
            #if file value is > time, then we want to use the power value on the line before
            elif (int(reg.group(1)) > time):
                power_vals[time] = power
                time += inc_t
            '''
            if (time > 8629200001):
                print "int version"
                print int(reg.group(1))
                print "string"
                print reg.group(1)
            '''
#    if (time > 8629200001):
#        break
#    if (time > 11629200001):
#        break
fpower.close()

fcnt = open('/home/david/cnt_vals.out', 'r')
print "Reading Counters"
time = 2292000000
for line in fcnt:
    #basically same deal as above, but now we have variable # of lines before a time value, so we have to check
    #the line to see if it contains #, then compare that time value to the internal value. Otherwise we do the 
    #same thing as the above loop. Store the counters in a dict, need some way to associate time with them

    #could update the dict every time value, so when we match the internal value, we just need to reference the dict. If file > internal, we just reference the dict first, then update the dict. That means we'd have to do the linear regression in this loop. Option two is to create a third dict, with time values as keys, and a counter tuple or something as the value 

    if '#' in line: 
        reg = re.match(r'#.*', line)
        if (reg != None):
            #if time = file time, then write to time dictionary
            if (int(line[1:]) >= time):
               counter_time[time] = counters.values()
               time += inc_t
    else:
        if line.strip(): 
            reg = re.match(r'(.{4,5}?): (.*)',line)
            key = reg.group(1)
            val = reg.group(2)
            counters[key] = val
#    if (time > 8629200001):
#        break

fcnt.close()
#print power_vals
#print counter_time
print "writing csv file"
fcsv = open('/home/david/data.csv', 'w')
fcsv.write('Time,Power,Cnt1,Cnt2,Cnt3,Cnt4,Cnt5,Cnt6,Cnt7,Cnt8,Cnt9\n')
#generate a .csv file to format the data
time = 2292000000
while (time< 57292000000):
#while (time< 8629200001):
   fcsv.write('%d,' %(time)) 
   l = counter_time[time]
   fcsv.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' %(power_vals[time], l[6], l[5], l[4], l[3], l[2], l[1], l[0], l[7], l[8]))
   time +=  inc_t
fcsv.close() 
