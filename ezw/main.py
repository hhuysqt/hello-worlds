import cv2
import numpy
import haar
import ezw

image = cv2.imread('a.jpg', cv2.IMREAD_GRAYSCALE)
img = image[0:512, 0:512]
(ox,oy) = img.shape

# Use signed 16-bit image to avoid overflow
img16 = numpy.asarray(img, dtype = numpy.int16)
trans = img16.copy()

# haar wavelet transform till 1 pixel
nround = 0
x,y = ox*2,oy*2
while x > 1 and y > 1:
    x = x/2
    y = y/2
    trans[0:x, 0:y] = haar.haar_wavelet(trans[0:x, 0:y], x,y)
    nround = nround+1

hrshow = numpy.asarray(trans, dtype = numpy.uint8)

# EZW encoding
positive_tr = trans.copy()
positive_tr[positive_tr < 0] = -positive_tr[positive_tr < 0]

tr_sign = trans.copy()

# Zerotree sign:   2'b00
# Isolate Zero     2'b01
tr_sign[trans == 0] = 1
# Positive symbol  2'b10
tr_sign[trans > 0] = 2
# Negative symbol  2'b11
tr_sign[trans < 0] = 3

# Start from the MSB
streamlen = numpy.zeros(8, dtype = numpy.int)
cmp_stream = numpy.zeros(8*ox*oy, dtype = numpy.uint8)
n = 0
cur_bit = 128
for i in range(8) :
    cur_band = positive_tr & cur_bit
    encode = ezw.iterate_band(cur_band, tr_sign)
    cmpband, size = ezw.compress_band_fast(encode)
    streamlen[i] = size
    cmp_stream[n:n+size] = cmpband[0:size]
    cur_bit = cur_bit/2
    n = n + size

print 'Each band:', streamlen
print 'Total:', streamlen.sum() / 4, 'bytes. Original', ox*oy, 'bytes.'


# EZW decoding
cur_bit = 256
decmp_tr = numpy.zeros((ox,oy), dtype = numpy.uint8)
n = 0
for i in range(8) :
    size = streamlen[i]
    cur_bit = cur_bit/2
    if size == 0:
        continue
    decmp_band = ezw.decompress_band_fast(cmp_stream[n:n+size], size, ox, oy)
    decmp_tr[decmp_band==2] = decmp_tr[decmp_band==2]+cur_bit
    decmp_tr[decmp_band==3] = decmp_tr[decmp_band==3]-cur_bit
    n = n+size

print 'decompress done. Difference:', (hrshow-decmp_tr).sum()

trans = numpy.asarray(decmp_tr, dtype = numpy.int16)

# inverse haar wavelet transform
x,y = 1,1
for i in range(nround):
    trans[0:x, 0:y] = haar.haar_wavelet_inv(trans[0:x, 0:y], x, y)
    x,y = x*2, y*2

result = numpy.asarray(trans, dtype = numpy.uint8)


cv2.imshow('original', img)
cv2.imshow('transform', hrshow)
cv2.imshow('decompressed', decmp_tr)
cv2.imshow('result', result)
while cv2.waitKey(0) != 32:
    continue
