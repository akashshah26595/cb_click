import subprocess
p = subprocess.Popen("./cinder_services.sh",stdout=subprocess.PIPE,shell=True)
(out,err) = p.communicate()
p_status = p.wait()
#tmp = proc.stdout.read()
#tmp = os.popen("./t.sh").read()
#print out
op = out.split()
for i in op:
            #x = i.strip('')
            print x
#print op

