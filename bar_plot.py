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

# labels = [u'Não Classificado', u'Bens Industriais', u'Comunicações', u'Consumo Cíclico', u'Consumo Não-cíclico', u'Financeiro',
         # u'Materiais Básicos', u'Petróleo, Gás e Biocombustíveis', u'Saúde', u'Tecnologia da Informação', u'Utilidade Pública']

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
colours = reorder(colours, original_indices)

plt.bar(labels, counts, width = 0.6, color = colours, edgecolor = 'black')

plt.xticks([x for x in range(len(labels))], labels, rotation = 90)
plt.subplots_adjust(bottom = 0.1, top = 0.98)
plt.savefig('bar.png')
