#from __future__ import print_function
import subprocess
p = subprocess.Popen("./cinder_services.sh",stdout=subprocess.PIPE,shell=True)
(out,err) = p.communicate()
p_status = p.wait()
#tmp = proc.stdout.read()
#tmp = os.popen("./t.sh").read()
#print out
op = out.split()
print(op)
k=0
for i in op:
	
	#x = i.strip('')
#       print("%s\t" %i)
#	print('a','b',sep='\t')
	if k==2:
		print "\n"
		k=0
	print("%-8s" %i),
	k+=1
		    	  
	#print op


