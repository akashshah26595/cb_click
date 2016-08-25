import subprocess
import shlex
cinder ="879a9ef1-2acc-4c73-b9d6-e84dcae0d31e" 
#p=subprocess.call(shlex.split("./check_glance.sh %s" %(cinder)))
#p=subprocess.(["./check_glance.sh",cinder],shell=True)
#Process=Popen('./childdir/execute.sh %s %s' % (str(var1),str(var2),), shell=True)
p = subprocess.Popen(('./check_glance.sh %s' %(cinder)),stdout=subprocess.PIPE,shell=True)
(out,err) = p.communicate()
print "OP:",out
p_statusNot  = p.wait()
op = str(out).strip()
print "Output:%s" %op
if op is None:
	print("Volume not Bootable or Glance Image Not Hosted On Cloudbyte")
else:
	print op
        print("Glance image is hosted on Cloudbyte")

