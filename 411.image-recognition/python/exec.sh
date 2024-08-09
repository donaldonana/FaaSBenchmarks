#!/bin/bash

# The list of library

MODEL=("resnet18" "resnet34" "resnet50" "resnet152")

IMAGE="1Mb.JPEG"
RESULT_FILE="result.txt"
ENERGY_DIR="Energy"
mkdir -p "$ENERGY_DIR/$IMAGE"
 
# Iterate over each word in the array
for RES in "${MODEL[@]}"; do

	wsk action update imgrec --timeout 300000 --memory 1024 --docker onanad/action-python-v3.9:imgrec __main__.py --web true 

    echo -e "$RES"  
    ENERGY_FILE="$ENERGY_DIR/$IMAGE/$RES$IMAGE.txt"  
    
    for (( i = 1; i <= 100; i++ )); do
    	 
    	# Launch cpu-energy-meter in background and save her PID
		cpu-energy-meter -r >> $ENERGY_FILE &
		METER_PID=$!
		wsk action invoke imgrec  --result  --param resnet "$RES" --param key $AWS_ACCESS_KEY_ID  --param access $AWS_SECRET_ACCESS_KEY --param image "$IMAGE" >> $RESULT_FILE
		kill -SIGINT $METER_PID
	
		echo -e "$i"
		
		# sleep 1
    done
    
done
