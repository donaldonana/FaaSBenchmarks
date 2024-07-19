#!/bin/bash

# The list of library
LIBRARY=("wand" "pygame" "opencv")
IMAGE="15Mb.JPEG"
RESULT_FILE="result.txt"
ENERGY_DIR="Energy"
mkdir -p "$ENERGY_DIR/$IMAGE"
 
# Iterate over each word in the array
for LIB in "${LIBRARY[@]}"; do

    echo -e "$LIB"  
    ENERGY_FILE="$ENERGY_DIR/$IMAGE/$LIB$IMAGE.txt"  
    
    for (( i = 1; i <= 100; i++ )); do
    	 
    	# Launch cpu-energy-meter in background and save her PID
	cpu-energy-meter -r >> $ENERGY_FILE &
	METER_PID=$!
	wsk action invoke thumb  --result  --param bib "$LIB" --param key $AWS_ACCESS_KEY_ID  --param access $AWS_SECRET_ACCESS_KEY --param file "$IMAGE" >> $RESULT_FILE
	kill -SIGINT $METER_PID
	
    done
    
done
