# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import json

def colour(rgba):
  return (rgba[0] / 255.0, rgba[1] / 255.0, rgba[2] / 255.0, rgba[3])

def reorder(array, indices):
  return [array[x] for x in indices]

with open('./classifications/2020/1.json', 'r') as f:
  data = f.read()
  parsed_data = json.loads(data)
  counts = [len(parsed_data[str(x)]) for x in range(-1, 9+1)]

print(counts)

# explode = (0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0) # explode 1st slice
explode = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
labels = ['NC', 'BI', 'Com', 'CC', 'CNC', 'Fin', 'MB', 'PGB', u'Saú', 'TI', 'UP']
colours = [
  colour([218, 64,  165, 0.9]),
  colour([252, 233, 22,  0.9]),
  colour([185, 255, 71,  0.9]),
  colour([81,  64,  255, 0.9]),
  colour([10,  144, 54,  0.9]),
  colour([22,  240, 252, 0.9]),
  colour([185, 144, 71,  0.9]),
  colour([81,  144, 165, 0.9]),
  colour([126, 73,  217, 0.9]),
  colour([252, 22,  26,  0.9]),
  colour([252, 114, 22,  0.9]),
]

original_indices = sorted(range(len(counts)), key = counts.__getitem__)
counts = reorder(counts, original_indices)
labels = reorder(labels, original_indices)
new_labels = []
for i in range(len(labels)):
  new_labels.append(labels[i] + ' (' + str(counts[i] / 100.0) + '%)')
colours = reorder(colours, original_indices)

fig = plt.figure(figsize = [8, 8])
ax = fig.add_subplot(111)

pie_wedge_collection = ax.pie(counts, colors = colours, labels = new_labels, labeldistance = 1.05);

for pie_wedge in pie_wedge_collection[0]:
  pie_wedge.set_edgecolor('white')

# plt.pie(counts, explode = explode, labels = labels, colors = colours, autopct = '%1.1f%%', startangle = 140)
# plt.pie(counts, colors = colours, startangle = 140, edgecolor = 'black')
plt.axis('equal')
plt.savefig('pie_chart.png')
