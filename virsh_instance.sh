sudo chmod +x virsh_check.sh
./virsh_check.sh | awk ' $2!="Name" {print $2}'