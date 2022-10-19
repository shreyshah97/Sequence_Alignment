from ctypes import alignment
import sys
import time
import psutil

def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)
    print(memory_consumed)
    return memory_consumed

def time_wrapper(driver_func):
    start_time = time.time()
    driver_func()
    end_time = time.time()
    time_taken = (end_time - start_time)*1000
    print(time_taken)
    process_memory()
    return time_taken

def read_file(input_file):
    """
    Reads the input file and returns the lines read.
    """
    with open(input_file, 'r') as f:
        lines = f.readlines()
        f.close()
    return lines
    
    
def generate_strings(lines):
    """
    Generates and returns the strings generated from the input file.
    """
    operation_counts = []
    base_lengths = []
    generated_strings = []
    count=0

    for line in lines:
        line = line.strip()
        if(not line.isnumeric()):
            if count != 0:
                generated_strings.append(base)
                operation_counts.append(count)
                count = 0
            base = line
            base_lengths.append(len(line))
        else:
            count += 1
            insert_at = int(line) + 1
            base = base[:insert_at] + base + base[insert_at:]
            
    generated_strings.append(base)
    operation_counts.append(count)
    return generated_strings, base_lengths, operation_counts

def validate_strings(generated_strings, base_lengths, operation_counts):
    """
    Validates string generated are of optimal length
    """
    inputs = list(zip(generated_strings, base_lengths, operation_counts))
    for input in inputs:
        if(len(input[0]) != (input[1] * int(2 ** input[2]))):
            print("Length of generated string is not 2^j")
            return -1

def initialize_variables():
    """
    Initializes the values of variables like delta and alpha
    """
    global DELTA, ALPHA
    DELTA = 30
    ALPHA = [[0,110,48,94],[110,0,118,48],[48,118,0,110],[94,48,110,0]]

def calculate_cost(generated_strings):
    """
    Calculates the minimum cost alignment for the sequences string1 and string2
    """
    string1, string2 = generated_strings
    string1_len = len(string1)
    string2_len = len(string2)
    dict = {"A":0, "C":1, "G":2, "T":3}
    dp = [[0] * (string1_len+1) for _ in range(0, string2_len+1)]

    for i in range(1, string1_len+1):
        dp[i][0] = i * DELTA
    for i in range(1, string2_len+1):
        dp[0][i] = i * DELTA

    #TODO: Check if i+1 instead of i makes more sense
    for i in range(1, string1_len+1):
        for j in range(1, string2_len+1):
            dp[i][j] = min(
                dp[i-1][j-1] + ALPHA[dict[string1[i-1]]][dict[string2[j-1]]], 
                DELTA + dp[i-1][j],
                DELTA + dp[i][j-1])

    print(dp[string1_len][string2_len])
    return dp

def calculate_alignment(generated_strings, dp):
    """
    Returns the aligned string for string1 and string2
    """
    string1, string2 = generated_strings
    i = len(string1)
    j = len(string2)
    dict = {"A":0, "C":1, "G":2, "T":3}
    aligned_string_1 = ""
    aligned_string_2 = ""
    
    while i!=0 and j!=0:
        if(dp[i][j] == dp[i-1][j-1] + ALPHA[dict[string1[i-1]]][dict[string2[j-1]]]):
            aligned_string_1 = string1[i-1] + aligned_string_1
            aligned_string_2 = string2[j-1] + aligned_string_2
            i-=1
            j-=1
        elif(dp[i][j] == DELTA + dp[i][j-1]):
            aligned_string_1 = "_" + aligned_string_1
            aligned_string_2 = string2[j-1] + aligned_string_2
            j-=1
        else:
            aligned_string_1 = string1[i-1] + aligned_string_1
            aligned_string_2 = "_" + aligned_string_2
            i-=1
    
    while i!=0:
        aligned_string_1 = string1[i-1] + aligned_string_1
        aligned_string_2 = "_" + aligned_string_2
        i-=1
    
    while j!=0:
        aligned_string_1 = "_" + aligned_string_1
        aligned_string_2 = string2[j-1] + aligned_string_2
        j-=1

    return [aligned_string_1, aligned_string_2]

def verify_cost(aligned_strings, dp):
    aligned_string_1, aligned_string_2 = aligned_strings
    aligned_string_len = len(aligned_string_1)
    cost=0
    dict = {"A":0, "C":1, "G":2, "T":3}

    for i in range(aligned_string_len):
        if(aligned_string_1[i] == '_' or aligned_string_2[i] == '_'):
            cost += DELTA
        else:
            cost += ALPHA[dict[aligned_string_1[i]]][dict[aligned_string_2[i]]]
    
    if dp[-1][-1] != cost:
        print("Minimum cost calculated does not match with the aligned sequence costs")
        return -1
    return cost


def driver():
    input_file_path = sys.argv[1] 
    output_file_path = sys.argv[2]
    initialize_variables()
    lines = read_file(input_file_path)
    generated_strings, base_lengths, operation_counts = generate_strings(lines)
    validate_strings(generated_strings, base_lengths, operation_counts)
    print(generated_strings[0]+"\n"+generated_strings[1])
    dp = calculate_cost(generated_strings)
    aligned_strings = calculate_alignment(generated_strings, dp)
    print(aligned_strings[0]+"\n"+aligned_strings[1])
    verify_cost(aligned_strings, dp)
    return

def main():
    time_wrapper(driver)

if __name__ == "__main__":
    main()