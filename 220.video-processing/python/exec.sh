#!/bin/bash

# The list of library
LIBRARY=("moviepy" "ffmpeg" "imageio" "opencv")
VIDEO="6Mb.avi"
RESULT_FILE="result.txt"
ENERGY_DIR="Energy"
mkdir -p "$ENERGY_DIR/$VIDEO"
 
# Iterate over each word in the array
for LIB in "${LIBRARY[@]}"; do

	wsk action update proc --docker  onanad/action-python-v3.9:proc __main__.py --web true -t 125000 -m 1024

    echo -e "$LIB"  
    ENERGY_FILE="$ENERGY_DIR/$VIDEO/$LIB$VIDEO.txt"  
    
    for (( i = 1; i <= 100; i++ )); do
    	 
    	# Launch cpu-energy-meter in background and save her PID
		cpu-energy-meter -r >> $ENERGY_FILE &
		METER_PID=$!
		wsk action invoke proc  --result  --param bib "$LIB" --param key $AWS_ACCESS_KEY_ID  --param access $AWS_SECRET_ACCESS_KEY --param file "$VIDEO" >> $RESULT_FILE
		kill -SIGINT $METER_PID
	
	echo -e "$i"
    done
    
done
