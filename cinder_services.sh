cinder service-list | awk '$10!="State" && $2!="Binary" {print $2 " " $10}'
#cinder service-list | awk '$10!="State" && $2!="Binary" && $4!="Host" {print $2 "\t " $4 "\t " $10}'
