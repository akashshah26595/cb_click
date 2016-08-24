import subprocess
import os
p = subprocess.Popen("./final.sh",stdout=subprocess.PIPE,shell=True)
(out,err) = p.communicate()
p_status = p.wait()
#tmp = proc.stdout.read()
#tmp = os.popen("./t.sh").read()
#print out
op = out.split()
arr = []
for i in op:
	x = i.strip('",')
	arr.append(x)
	#print x
print arr[1]		
#print op

