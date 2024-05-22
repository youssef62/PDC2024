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

if __name__ == '__main__':
    # get signal.txt
    x = np.loadtxt("signal.txt")
    print(x)
    y = channel(x)
    print(y)
    np.savetxt("rcvd_signal.txt", y, fmt='%f')