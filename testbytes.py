z = "hey hi"

a = bytes(z,'utf-8')
b = b'second sentence in bytes'
c = a+b'stringsplit'+b
print(len(c.split(b'stringsplit')))

# import numpy as np
# d = np.arange(0)
# arr = np.array([[[1, 2, 9],[3, 7, 4]], [[5, 6, 0], [7, 8, 1]], [[5, 6, 0], [7, 8, 1]], [[5, 6, 0], [7, 8, 1]]])
# shape = (720, 1280, 3)
# bite = bytes(str(shape[1]),'utf-8')
# print(type(bite.decode()))