cinder service-list | awk '$10!="State" && $2!="Binary" {print $2 " " $10}'

