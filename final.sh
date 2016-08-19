cinder list | awk ' NF > 1 && $2 != "ID" && $12 ~ /^cb-/ && $14=="true" {print $18}'   | nova show "$(awk '{print $1}')"   | awk '$2 == "os-extended-volumes:volumes_attached" {cind_id = $5} $2 =="OS-EXT-SRV-ATTR:instance_name" {virsh_id=$4} $2 == "id" {nova_id= $4} \
	END {print cind_id " " virsh_id " " nova_id}'
