import math 
import matplotlib.pyplot as plt
import numpy as np
F = 20*10**9

us = 30*10**6
di = 2*10**6
N = [10, 100, 1000]
u = [300*10**3, 700*10**3, 2*10**6]
table = []
for i in N:
    T = max(i*F/us,F/di)
    print(i*F/us,F/di)
    #print(T)

for i in N:
    for k in u:
        T = max(F/us,F/di,i*F/(us+i*k))
        #print(F/us,F/di,i*F/(us+i*k))
        print(T)
        table.append(T)
print(table)
data = [[table.pop(0),table.pop(0),table.pop(0)],
        [table.pop(0),table.pop(0),table.pop(0)],
        [table.pop(0),table.pop(0),table.pop(0)]]
print(data)

columns = u
rows = ('10', '100', '1000')

# Get some pastel shades for the colors
colors = plt.cm.BuPu(np.linspace(0, 0.5, len(rows)))
n_rows = len(data)
  
index = np.arange(len(columns)) + 0.3
bar_width = 0.4
  
# Initialize the vertical-offset for
# the line plots.
y_offset = np.zeros(len(columns))
  
# Plot line plots and create text labels 
# for the table
cell_text = []
for row in range(n_rows):
    plt.plot(index, data[row], color=colors[row])
    y_offset = data[row]
    cell_text.append([x for x in y_offset])
  
# Reverse colors and text labels to display
# the last value at the top.
colors = colors[::-1]
cell_text.reverse()
  
# Add a table at the bottom of the axes
the_table = plt.table(cellText=cell_text,
                      rowLabels=rows,
                      rowColours=colors,
                      colLabels=columns,
                      loc='bottom')
  
# Adjust layout to make room for the table:
plt.subplots_adjust(left=0.2, bottom=0.2)
  
plt.ylabel("Time")
plt.xticks([])
plt.title('N with respect to u')
  
plt.show()