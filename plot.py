import matplotlib.pyplot as plt
import json
import sys
  
input_count = int(sys.argv[1])
file_name = sys.argv[2]

with open(file_name, 'r') as f:
    metric_data = json.loads(f.read())
    f.close()


x1 = metric_data['basic']['time_taken']
x2 = metric_data['efficient']['time_taken']
y = []
for i in range (0, input_count):
    y.append("input" + str(i+1))

fig, axis = plt.subplots(2)
axis[0].plot(x1, y)
axis[0].plot(x2, y)

memory1 = metric_data['basic']['memory_consumed']
memory2 = metric_data['efficient']['memory_consumed']

axis[1].plot(memory1, y)
axis[1].plot(memory2, y)

plt.show()