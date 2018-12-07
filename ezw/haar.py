# the simplest haar wavelet transform
import numpy

def haar_FWT(trans) :
    (x, y) = trans.shape
    x,y = x*2,y*2
    while x > 1 and y > 1:
        x = x/2
        y = y/2
        trans[0:x, 0:y] = haar_wavelet(trans[0:x, 0:y], x,y)

    return trans

def inv_haar_FWT(trans) :
    (xsize, ysize) = trans.shape
    x,y = 1,1
    while x <= xsize and y <= ysize:
        trans[0:x, 0:y] = haar_wavelet_inv(trans[0:x, 0:y], x, y)
        x,y = x*2, y*2

    return trans

def haar_wavelet(a,x,y):
    b = a.copy()
    b[0:x/2] = (a[0:x-1:2] + a[1:x:2])/2
    b[x/2:(x|1)-1] = (a[0:x-1:2] - a[1:x:2])/2
    c = b.copy()
    c[...,0:y/2] = (b[...,0:y-1:2] + b[...,1:y:2])/2
    c[...,y/2:(y|1)-1] = (b[...,0:y-1:2] - b[...,1:y:2])/2
    return c

def haar_wavelet_inv(c,x,y):
    d = c.copy()
    d[...,0:y-1:2] = c[...,0:y/2] + c[...,y/2:(y|1)-1]
    d[...,1:y:2] = c[...,0:y/2] - c[...,y/2:(y|1)-1]
    e = d.copy()
    e[0:x-1:2] = d[0:x/2] + d[x/2:(x|1)-1]
    e[1:x:2] = d[0:x/2] - d[x/2:(x|1)-1]
    return e
