import numpy

def determine_if_zerotree(parent, children) :
    tmp = numpy.zeros(parent.shape, dtype = numpy.uint8)
    # First set it to isolate zero
    tmp[parent == 0] = 1
    # Determine if all of its 4 children are zerotree
    (cx, cy) = children.shape
    zt = children[0:cx-1:2, 0:cy-1:2] | children[0:cx-1:2, 1:cy:2] | \
         children[1:cx:2,   0:cy-1:2] | children[1:cx:2,   1:cy:2]
    zt[zt != 0] = 3
    # Change to zerotree if children are zerotree
    tmp = tmp & zt
    return tmp

def iterate_band(cur_band, tr_sign):
    (xmax, ymax) = cur_band.shape
    encode = numpy.zeros(cur_band.shape, dtype = numpy.uint8)
    encode[cur_band!=0] = tr_sign[cur_band!=0]

    # Determine zerotree on the ll band
    llx, lly = xmax/2, ymax/2
    while llx > 1 and lly > 1:
        # On hl, lh, hh bands, set zerotree if 4 childnodes are all zerotree
        hl = encode[llx/2:llx, 0:lly/2]
        lh = encode[0:llx/2, lly/2:lly]
        hh = encode[llx/2:llx, lly/2:lly]
        encode[llx/2:llx, 0:lly/2] = hl | determine_if_zerotree(hl, encode[llx:llx*2, 0:lly])
        encode[0:llx/2, lly/2:lly] = lh | determine_if_zerotree(lh, encode[0:llx, lly:lly*2])
        encode[llx/2:llx, lly/2:lly] = hh | determine_if_zerotree(hh, encode[llx:llx*2, lly:lly*2])
        llx, lly = llx/2, lly/2
    if encode[0,0] == 0 :
        if encode[1,0] != 0 or encode[0,1] != 0 or encode[1,1] != 0:
            # The root is not zerotree
            encode[0,0] = 1
    return encode

def form_index(i) :
    return (i & 1) + ((i & 4)>>1) + ((i & 16)>>2) + ((i & 64)>>3) + \
           ((i&256)>>4) + ((i&1024)>>5) + ((i&4096)>>6) + ((i&16384)>>7) + \
           ((i&65536)>>8) + ((i&262144)>>9) + ((i&1048576)>>10)

def compress_band_fast(encode) :
    if encode[0,0] != 0 :
        xsize, ysize = encode.shape
        cmpband = numpy.zeros(xsize*ysize, dtype = numpy.uint8)
        cmpband[0] = encode[0,0]
        n = 1

        # Iterate the tree in First-Root order
        i, mask = 1, 3
        while i > 0 :
            xindex, yindex = form_index(i), form_index(i>>1)
            thiscode = encode[xindex, yindex]
            cmpband[n] = thiscode
            n = n+1
            if thiscode == 0 or \
               xindex*2+1 > xsize or yindex*2+1 > ysize :
                # This is a zerotree root, or the end node
                i = (i + 1) & mask
                while mask != 0 and i & 3 == 0 :
                    # Back to the parent node
                    i = i >> 2
                    mask = mask >> 2
            else :
                # Head for the child node
                i = i << 2
                mask = (mask << 2) | 3
    
        #print cmpband[0:n]
        return cmpband[0:n], n

    else :
        return [], 0

def decompress_band_fast(cmpband, cmpsize, xsize, ysize) :
    decmp = numpy.zeros((xsize,ysize), dtype = numpy.uint8)
    if cmpsize != 0 :
        decmp[0,0] = cmpband[0]
        n = 1

        # Iterate through the tree in first-root order
        i, mask = 1, 3
        while i > 0 :
            xindex, yindex = form_index(i), form_index(i>>1)
            thiscode = cmpband[n]
            decmp[xindex, yindex] = thiscode
            n = n+1
            if thiscode == 0 or \
               xindex*2+1 > xsize or yindex*2+1 > ysize :
                # This is a zerotree root, or the end node
                i = (i + 1) & mask
                while mask != 0 and i & 3 == 0 :
                    # Back to the parent node
                    i = i >> 2
                    mask = mask >> 2
            else :
                # Head for the child node
                i = i << 2
                mask = (mask << 2) | 3
    return decmp


def ezw_encode(trans) :
    tr_sign = trans.copy()

    # Zerotree sign:   2'b00
    # Isolate Zero     2'b01
    tr_sign[trans == 0] = 1
    # Positive symbol  2'b10
    tr_sign[trans > 0] = 2
    # Negative symbol  2'b11
    tr_sign[trans < 0] = 3

    trans[trans < 0] = -trans[trans < 0]
    streamlen = numpy.zeros(8, dtype = numpy.int)
    cmp_stream = numpy.zeros(8*trans.size, dtype = numpy.uint8)

    # Start from the MSB
    n = 0
    cur_bit = 128
    for i in range(8) :
        cur_band = trans & cur_bit
        encode = iterate_band(cur_band, tr_sign)
        cmpband, size = compress_band_fast(encode)
        streamlen[i] = size
        cmp_stream[n:n+size] = cmpband[0:size]
        cur_bit = cur_bit/2
        n = n + size

    return cmp_stream[0:n], streamlen

def ezw_decode(cmp_stream, streamlen, xsize, ysize) :
    cur_bit = 256
    decmp_tr = numpy.zeros((xsize,ysize), dtype = numpy.uint8)
    n = 0
    for i in range(8) :
        size = streamlen[i]
        cur_bit = cur_bit/2
        if size == 0:
            continue
        decmp_band = decompress_band_fast(cmp_stream[n:n+size], size, xsize, ysize)
        decmp_tr[decmp_band==2] = decmp_tr[decmp_band==2]+cur_bit
        decmp_tr[decmp_band==3] = decmp_tr[decmp_band==3]-cur_bit
        n = n+size

    return decmp_tr
