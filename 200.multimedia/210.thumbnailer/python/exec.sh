#!/bin/bash

# The list of library
library=("pillow" "wand" "pygame" "opencv")

RESULT_FILE="result.txt"
ENERGY_DIR="Energy"
mkdir -p "$ENERGY_DIR"
 
# Iterate over each word in the array
for lib in "${library[@]}"; do

    echo -e "$lib"  
    ENERGY_FILE="$ENERGY_DIR/$lib.txt"  
    
    for (( i = 1; i <= 10; i++ )); do
    	 
    	# Launch cpu-energy-meter in background and save her PID
	cpu-energy-meter -r >> $ENERGY_FILE &
	METER_PID=$!
	wsk action invoke thumb  --result  --param bib "$lib" --param key $AWS_ACCESS_KEY_ID  --param access $AWS_SECRET_ACCESS_KEY >> $RESULT_FILE
	kill -SIGINT $METER_PID
	
    done
    
done
