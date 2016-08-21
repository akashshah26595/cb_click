import subprocess
import shlex

#p = subprocess.Popen(["./freeze.sh","instance-00000002"],stdout=subprocess.PIPE,shell=True)
#(out,err) = p.communicate()

# ./virsh_check.sh | awk ' $2!="Name" {print $2}'
inst = 'instance-00000002'
p=subprocess.call(shlex.split('./freeze.sh %s' %(inst)))
#p_status = p.wait()
#tmp = proc.stdout.read()
#tmp = os.popen("./t.sh").read()
#print out
#op = out.split()
#for i in op:
#            x = i.strip('",')

#            print x
#print op

