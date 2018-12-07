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

def compress_band(encode) :
    (x,y) = encode.shape
    n = 0
    cmpband = numpy.zeros(x*y, dtype = numpy.uint8)
    for i in range(x*y) :
        xindex = form_index(i)
        yindex = form_index(i>>1)
        #print '(',xindex,yindex,')',
        if encode[xindex, yindex] == 0 :
            # Check whether the father is also a zero tree
            if encode[xindex/2, yindex/2] != 0 :
                cmpband[n] = 0
                n = n+1
            else :
                i = i+4
        else :
            cmpband[n] = encode[xindex, yindex]
            n = n+1
    #print ' '
    #print 'Total:', n, 'codes.'
    #print cmpband[0:n]
    return cmpband[0:n], n

def decompress_band(cmpband, cmpsize, xsize, ysize) :
    decmp = numpy.zeros((xsize,ysize), dtype = numpy.uint8)
    decmp[0,0] = cmpband[0]
    n = 0
    for i in range(xsize*ysize) :
        xindex = form_index(i)
        yindex = form_index(i>>1)
        if decmp[xindex/2, yindex/2] != 0 :
            decmp[xindex, yindex] = cmpband[n]
            #print '(',xindex,yindex,')',
            n = n+1
    #print ' '
    #print 'Filled', n, 'codes.'
    #print decmp
    return decmp

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