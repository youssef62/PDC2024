import numpy as np
import random
def channel(x):
    n = x.size
    B = random.choice([0, 1])
    sigma_sq = 25
    Z = np.random.normal(0, np.sqrt(sigma_sq), (2*n))
    X = np.zeros(2*n)
    if B == 1:
        X[0:n] = x
    else:
        X[n:2*n] = x
    Y=X+Z
    Y = np.reshape(Y, (-1))
    return Y

def server_simulation(input_path, output_path):
    # get signal.txt
    x = np.loadtxt(input_path)
    print("the energy of the signal is #chunks * energy of codeword for a observation: ", np.sum(np.square(np.abs(x))))
    y = channel(x)
    np.savetxt(output_path, y, fmt='%f')
