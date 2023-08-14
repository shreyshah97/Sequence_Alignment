import json
import sys

file_name = sys.argv[1]

with open(file_name, 'w') as f:
    dict = {
        "basic": {
            "time_taken": [],
            "memory_consumed": []
        },
        "efficient": {
            "time_taken": [],
            "memory_consumed": []
        },
        "input_size": []
    }
    f.write(json.dumps(dict, indent=4))
    f.close()