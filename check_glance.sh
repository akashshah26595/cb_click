cind=$1
#awk -v var="$variable" 'BEGIN {print var}'
#pactl list short sinks | awk -v myvar="$usb_soundcard_sink" '$2==myvar {print $1}'
cinder list | awk -v myvar="$cind" '$2==myvar && $14 =="true" {print $12}'
