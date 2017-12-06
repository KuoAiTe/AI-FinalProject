import numpy as np

content = np.random.randint(0, 2, (20, 100))
content = '[0, 1, 2]'
file_object = open('B.txt', 'w')
file_object.write(content)
file_object.close()