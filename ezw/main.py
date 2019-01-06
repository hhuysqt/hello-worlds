# - Haar FWT
# - EZW encoding
# - EZW decoding
# - Inverse Haar FWT

import cv2
import numpy
import haar
import ezw
import sys, getopt
import entropy

if __name__ == "__main__":
    dumpmode = 0
    filename = 'a.jpg'
    output = 0
    outfile = 'a.ezw'
    disp = 0
    dispfile = ''

    opts,args = getopt.getopt(sys.argv[1:], 'htd:i:o:')
    if len(opts) == 0:
        print 'Use default image:', filename
    else :
        for o,v in opts :
            if o == '-i' :
                filename = v
            elif o == '-t' :
                # test mode: output the compression rate in csv form
                dumpmode = 1
            elif o == '-o' :
                output = 1
                outfile = v
            elif o == '-d' :
                # uncompress and display the file
                disp = 1
                dispfile = v
            else :
                print 'Usage: python', sys.argv[0], '[OPTION] [FILE]'
                print '-h          show this manual'
                print '-t          test mode: show compression rate in csv'
                print '-i <file>   input file'
                print '-o <file>   output compressed file'
                print '-d <file>   uncompress and display the file'
                sys.exit()

    if disp == 0 :
        image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
        
        # Strip to 512x512
        (ox,oy) = image.shape
        if ox > 512 and oy > 512:
            sx, sy = (ox-512)>>1, (oy-512)>>1
            img = image[sx:sx+512, sy:sy+512]
        else :
            img = cv2.resize(image, (512,512))
        (ox,oy) = img.shape

        # Use signed 16-bit image to avoid overflow
        img16 = numpy.asarray(img, dtype = numpy.int16)
        trans = img16.copy()

        # haar wavelet transform till 1 pixel
        trans = haar.haar_FWT(trans)
        hrshow = numpy.asarray(trans, dtype = numpy.uint8)

        # EZW encoding
        cmp_stream, streamlen = ezw.ezw_encode(trans)
        if output == 1 :
            cmprsfile = open(outfile, 'wb')
            xy = numpy.zeros(2, dtype = numpy.int)
            xy[0] = ox
            xy[1] = oy
            numpy.save(cmprsfile, xy)
            numpy.save(cmprsfile, streamlen)
            numpy.save(cmprsfile, cmp_stream)
            cmprsfile.close()

        # calculate the entropy to measure compression
        ent = entropy.calc_entropy(img)
        print filename, ',', ent/8, ',', streamlen.sum()/4.0/ox/oy
    else :
        cmprsfile = open(dispfile, 'rb')
        xy = numpy.load(cmprsfile)
        ox, oy = xy[0], xy[1]
        streamlen = numpy.load(cmprsfile)
        cmp_stream = numpy.load(cmprsfile)
        cmprsfile.close()

    if dumpmode == 0 or disp == 1:
        # EZW decoding
        print 'Decompressing...'
        decmp_tr = ezw.ezw_decode(cmp_stream, streamlen, ox, oy)
        print 'Done.'

        # inverse haar wavelet transform
        trans = numpy.asarray(decmp_tr, dtype = numpy.int16)
        trans = haar.inv_haar_FWT(trans)
        result = numpy.asarray(trans, dtype = numpy.uint8)

        if disp == 0 :
            cv2.imshow('original', img)
            cv2.imshow('transform', hrshow)
        cv2.imshow('decompressed', decmp_tr)
        cv2.imshow('result', result)
        while cv2.waitKey(0) != 32:
            continue
