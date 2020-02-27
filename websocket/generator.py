
import numpy as np
import time


while True:
	dataFile = open("./data.txt",'a')
	k = np.random.randint(0,high=2)
	k = str(k)
	print(k)
	dataFile.write(k)
	dataFile.close()
	time.sleep(1)
