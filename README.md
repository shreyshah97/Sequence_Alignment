# CSCI-570-Analysis-of-Algorithms

The repository contains the code for the final project - Sequence Alignment Problem for the course CSCI 570 offered in Fall 2022 at USC - Analysis of Algorithms. This course was taught by Prof. Shamsian.

## Project Details

The Project Details directory contains the pdf of the project based on the Sequence Alignment Problem.
We are solving the sequence alignment problem via 2 methods, we initially solve the problem via dynamic programming without space restritions and then optimize the approach to use minimal space by performing divide and conquer on the original method.
There are sample test cases and datapoints in the directory, on which we run the scripts - basic_3.py and efficient_3.py
Summary.docx contains the information about time taken to run strings of different lengths and the time and space taken by each method, along with the graphs.

## Running the code

1. We run the `script.sh` with an argument suggesting the number of test cases to run from the given datapoints.
2. It will create a `metrics.json` file containing the space and time taken by each approach for various length strings.
3. Based on the `metrics.json` file we internally call the `plot_time.py` and `plot_memory.py` which will generate plots for the time and memory consumed by these approaches.
