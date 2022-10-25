#!/bin/bash

inputCount=$1
efficientFile="./efficient_3.py"
basicFile="./basic_3.py"

python3 "clear_metrics.py" $1

for (( c=1; c<=inputCount; c++ ))
do 
    inputFileName="./Project_Details/SampleTestCases/input"$c".txt"
    outputBasicFileName="./Project_Details/SampleTestCases/output_basic"$c".txt"
    outputEfficientFileName="./Project_Details/SampleTestCases/output_efficient"$c".txt"
    python3 "$basicFile" "$inputFileName" "$c" "$outputBasicFileName" "metrics.json"
    python3 "$efficientFile" "$inputFileName" "$c" "$outputEfficientFileName" "metrics.json"
done

python3 "plot.py" $1 "metrics.json"
