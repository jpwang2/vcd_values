import sys
import re

counters = {} 
f = open('/home/david/counters.vcd', 'r')
fw = open('/home/david/cnt_vals.out', 'w')
flag = 0
for line in f:
#search specifically for counter values(which are all 32 bit)
    if ('module' in line and flag < 3):
        flag+=1 
    elif ('module' in line and flag == 3):
        reg = re.search(r'module (.{4,5}?) .*', line)
        name = reg.group(1)
        
    elif 'var reg' in line:
        counter = re.search(r'var reg 32 (.?) .*',line)     
        symbol = counter.group(1)
        counters[symbol] = name 
    #found a time value
    elif '#' in line: 
        reg = re.match(r'#.*', line)
        if (reg != None):
            fw.write(line)
    else
        reg = re.match(r'(.*) (.?)',line)
        reg.group(1) #the value
        reg.group(2) #the counter key
    
print counters
f.close()
fw.close()
