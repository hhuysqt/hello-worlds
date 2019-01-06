import numpy as np
import math

def calc_entropy(data) :
  stat = np.zeros(256, dtype = float)
  for i in range(256) :
    tmp = np.zeros(data.shape)
    tmp[data == i] = 1
    stat[i] = np.count_nonzero(tmp)
  stat = stat / data.size

  # calculate the entropy
  entropy = 0
  for p in stat :
    if p > 0 :
      entropy = entropy - p * math.log(p, 2)

  return entropy
