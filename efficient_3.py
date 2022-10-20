from ctypes import alignment
import string
import sys
import time
import psutil

dict = {"A":0, "C":1, "G":2, "T":3}

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

def calculate_cost(string1, string2):
    """
    Calculates the minimum cost alignment for the sequences string1 and string2
    """
    string1_len = len(string1)
    string2_len = len(string2)
    dp = [[0] * (2) for _ in range(0, string1_len+1)]

    for i in range(1, string1_len+1):
        dp[i][0] = i * DELTA

    #TODO: Check if i+1 instead of i makes more sense
    for j in range(1, string2_len+1):
        dp[0][1] = (j) * DELTA
        for i in range(1, string1_len+1):
           dp[i][1] = min(
                dp[i-1][0] + ALPHA[dict[string1[i-1]]][dict[string2[j-1]]], 
                DELTA + dp[i-1][1],
                DELTA + dp[i][0])
        for k in range(0, string1_len+1):
            dp[k][0] = dp[k][1]

    return dp

def calculate_optimal_cut(string1, string2):
    """
    Calculates the optimal cut for Y when X is divided into 2 halves
    """
    string1_len = len(string1)
    string1_left = string1[:int(string1_len/2)]
    string1_right = string1[int(string1_len/2):]
    dp_left = calculate_cost(string2, string1_left)
    dp_right = calculate_cost(string2[::-1], string1_right[::-1])
    dp_left_len = len(dp_left)
    min = sys.maxsize
    min_index = 0

    for i in range(dp_left_len):
        if(dp_left[i][1] + dp_right[dp_left_len-i-1][1]<min):
            min = dp_left[i][1] + dp_right[dp_left_len-i-1][1]
            min_index = i

    return min_index

def calculate_alignment(string1, string2):
    """
    Returns the aligned string for string1 and string2
    """
    string1_len = len(string1)
    string2_len = len(string2)
    aligned_string_1 = ""
    aligned_string_2 = ""
    if string1_len == 1:
        if string2_len == 0:
            aligned_string_1 = string1[0]
            aligned_string_2 = '_'
        elif string2_len == 1:
            if ALPHA[dict[string1[0]]][dict[string2[0]]] < (2 * DELTA):
                aligned_string_1 = string1[0]
                aligned_string_2 = string2[0]
            else:
                aligned_string_1 = '_'+string1[0]
                aligned_string_2 = string2[0]+'_'
        else:
            s_unique = set(string2)
            min_cost = min(ALPHA[dict[char]][dict[string1[0]]] for char in s_unique)

            if 2 * DELTA <= min_cost:
                aligned_string_1 = "_" * (len(string2)) + string1
                aligned_string_2 = string2 + "_"
                
            else:
                char_idx = [i for i, cost in enumerate(ALPHA[dict[string1]]) if cost == min_cost]
                matched_char = None
                for char, i in dict.items():
                    if i == char_idx[0]:
                        matched_char = char
                idx = string2.find(str(matched_char))    
                aligned_string_1 = '_' * (idx) + string1 + '_' * (len(string2)-idx-1)
                aligned_string_2 = string2         
        return aligned_string_1, aligned_string_2
    
    index = calculate_optimal_cut(string1, string2)
    aligned_string_left_1, aligned_string_left_2 = calculate_alignment(string1[:int(string1_len/2)], string2[:index])
    aligned_string_right_1, aligned_string_right_2 = calculate_alignment(string1[int(string1_len/2):], string2[index:])
    aligned_string_1, aligned_string_2 = aligned_string_left_1 + aligned_string_right_1, aligned_string_left_2 + aligned_string_right_2
    return aligned_string_1, aligned_string_2

def verify_cost(aligned_string_1, aligned_string_2):
    aligned_string_len = len(aligned_string_1)
    cost=0

    for i in range(aligned_string_len):
        if(aligned_string_1[i] == '_' or aligned_string_2[i] == '_'):
            cost += DELTA
        else:
            cost += ALPHA[dict[aligned_string_1[i]]][dict[aligned_string_2[i]]]
    
    print(cost)
    return cost

def driver():
    input_file_path = sys.argv[1] 
    output_file_path = sys.argv[2]
    initialize_variables()
    lines = read_file(input_file_path)
    generated_strings, base_lengths, operation_counts = generate_strings(lines)
    validate_strings(generated_strings, base_lengths, operation_counts)
    print(generated_strings[0]+"\n"+generated_strings[1])
    aligned_string_1, aligned_string_2 = calculate_alignment(generated_strings[0], generated_strings[1])
    verify_cost(aligned_string_1, aligned_string_2)
    print(aligned_string_1+"\n"+aligned_string_2)
    return

def main():
    time_wrapper(driver)

if __name__ == "__main__":
    main()