import numpy as np 
import GenerateDataset as gd


for i in range(1001):
    print(f"Generating data: {i} ---")
    dist = np.random.uniform(200,1000)
    m1 = dist * 0.07 + np.random.uniform(-10, 30)
    m2 = dist * 0.07 + np.random.uniform(-10, 30)
    spin1 = np.random.uniform(0,0.9)
    spin2 = np.random.uniform(0,0.9)
    number = np.random.randint(1, 10)

    if number >= 2:
        gd.FakeNoise(6, int(2048 / (1.0/16)) + 1, 1.0/ 16, 1.0/4096, int(32/(1.0/4096)), i)
    else:
        gd.Signal(6, int(2048 / (1.0/16)) + 1, 1.0/ 16, 1.0/4096, int(32/(1.0/4096)), i, m1, m2, dist, spin1, spin2)