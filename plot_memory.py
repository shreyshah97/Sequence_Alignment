import matplotlib.pyplot as plt
import json
import sys

input_count = int(sys.argv[1])
file_name = sys.argv[2]

with open(file_name, 'r') as f:
    metric_data = json.loads(f.read())
    f.close()
  
# create data
memory1 = metric_data['basic']['memory_consumed']
memory2 = metric_data['efficient']['memory_consumed']
x = metric_data['input_size']
  
# plot lines
plt.plot(x, memory1, label = "line 1")
plt.plot(x, memory2, label = "line 2")
plt.xlabel("Input Size", fontsize=12)
plt.ylabel("Memory Usage in KB", fontsize=12)
plt.title("Memory Usage vs Problem Size")
labels = ["Basic", "Efficient"]
plt.legend(labels = labels)
plt.show()