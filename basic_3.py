import sys

def generate_string(input_file):
    """
    Generates and returns the strings generated from the input file.
    """
    with open(input_file, 'r') as f:
        count=0
        while True:
            line = f.readline().strip()
            if not line:
                break
            if(not line.isnumeric()):
                if count!=0:
                    string1 = base
                    if(len(string1)!=(base_length*int(2**count))):
                        print("Length of generated string is not 2^j")
                    count=0
                base = line
                base_length = len(line)
            else:
                count+=1
                breakpt = int(line)+1
                base = base[:breakpt] + base + base[breakpt:]
            
    string2 = base
    if(len(string2)!=(base_length*int(2**count))):
        print("Length of generated string is not 2^k")
    count=0
    return string1, string2

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
    print(string1+"\n"+string2)
    m = len(string1)
    n = len(string2)
    dict = {"A":0, "C":1, "G":2, "T":3}
    dp = [[0] * (m+1) for _ in range(0, n+1)]
    for i in range(1,m+1):
        dp[i][0] = i*DELTA
    for i in range(1,n+1):
        dp[0][i] = i*DELTA

    for i in range(1,m+1):
        for j in range(1,n+1):
            dp[i][j] = min(dp[i-1][j-1]+ALPHA[dict[string1[i-1]]][dict[string2[j-1]]], DELTA+dp[i-1][j], DELTA+dp[i][j-1])

    print(dp)
    return dp[m][n]


def main():
    input_file= sys.argv[1] 
    output_file= sys.argv[2]
    initialize_variables()
    string1, string2 = generate_string(input_file)
    print(string1+"\n"+string2)
    calculate_cost(string1,string2)
    return

if __name__ == "__main__":
    main()