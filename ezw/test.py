import numpy

def do(num):
  print num,

def iterate_heap(heap, size) :
  do(heap[0])

  i, mask = 1, 1
  while i > 0 :
    do(heap[i])
    if i*2+1 > size :
      i = (i+1) & mask
      while mask != 0 and (i & 1) == 0 :
        i, mask = i >> 1, mask >> 1
    else :
      i, mask = i << 1, mask << 1 | 1

if __name__ == '__main__':
  a = numpy.arange(16)
  iterate_heap(a, 16)
