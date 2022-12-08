#!/bin/bash

inputCount=$1
efficientFile="./efficient_3.py"
basicFile="./basic_3.py"

python3 "./clear_metrics.py" "metrics.json"

for (( c=1; c<=inputCount; c++ ))
do 
    inputFileName="./Project_Details/datapoints/in"$c".txt"
    outputBasicFileName="./Project_Details/datapoints/output_basic"$c".txt"
    outputEfficientFileName="./Project_Details/datapoints/output_efficient"$c".txt"
    python3 "$basicFile" "$inputFileName" "$outputBasicFileName"
    python3 "$efficientFile" "$inputFileName" "$outputEfficientFileName"
done

python3 "plot_time.py" $(($1 + 1)) metrics.json
python3 "plot_memory.py" $(($1 + 1)) metrics.json
