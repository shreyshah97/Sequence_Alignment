import matplotlib.pyplot as plt
import json
import sys

input_count = int(sys.argv[1])
file_name = sys.argv[2]

with open(file_name, 'r') as f:
    metric_data = json.loads(f.read())
    f.close()
  
# create data
time1 = metric_data['basic']['time_taken']
time2 = metric_data['efficient']['time_taken']
x = metric_data['input_size']
  
# plot lines
plt.plot(x, time1, label = "line 1")
plt.plot(x, time2, label = "line 2")
plt.xlabel("Input Size", fontsize=12)
plt.ylabel("Time Taken in Milli Seconds", fontsize=12)
plt.title("CPU Time vs Problem Size")
labels = ["Basic", "Efficient"]
plt.legend(labels = labels)
plt.show()