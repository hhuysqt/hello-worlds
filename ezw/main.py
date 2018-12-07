# - Haar FWT
# - EZW encoding
# - EZW decoding
# - Inverse Haar FWT

import cv2
import numpy
import haar
import ezw
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print 'Use default image: a.jpg'
        image = cv2.imread('a.jpg', cv2.IMREAD_GRAYSCALE)
    else :
        image = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
    
    # Strip to 512x512
    img = image[0:512, 0:512]
    (ox,oy) = img.shape

    # Use signed 16-bit image to avoid overflow
    img16 = numpy.asarray(img, dtype = numpy.int16)
    trans = img16.copy()

    # haar wavelet transform till 1 pixel
    trans = haar.haar_FWT(trans)
    hrshow = numpy.asarray(trans, dtype = numpy.uint8)

    # EZW encoding
    cmp_stream, streamlen = ezw.ezw_encode(trans)
    print 'Each band:', streamlen
    print 'Total:', streamlen.sum() / 4, 'bytes. Original', ox*oy, 'bytes.'


    # EZW decoding
    decmp_tr = ezw.ezw_decode(cmp_stream, streamlen, ox, oy)
    print 'decompress done. Difference:', (hrshow-decmp_tr).sum()

    # inverse haar wavelet transform
    trans = numpy.asarray(decmp_tr, dtype = numpy.int16)
    trans = haar.inv_haar_FWT(trans)
    result = numpy.asarray(trans, dtype = numpy.uint8)


    cv2.imshow('original', img)
    cv2.imshow('transform', hrshow)
    cv2.imshow('decompressed', decmp_tr)
    cv2.imshow('result', result)
    while cv2.waitKey(0) != 32:
        continue
