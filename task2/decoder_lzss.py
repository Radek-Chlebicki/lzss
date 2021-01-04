import sys;
# Radek Chlebicki 29175224



import huffman
import eliasc
# how to convert z algorithm for lzss
# can we use ukkonen

# function that given the start of the window, window size , start of look ahead, look ahead size returns
# the lz77 tuple

"""
the lzss decoding decodes the bits using elias or huffman
complexity: 
elias decoding O(e) huffman decoding O(h) (o and e are the number of bits in the encodings) 
decoding + building the string O(n) where n is the number of bits in the compressed form 
space: O(n) as a new string is built.  

"""


def decoding(encodedlist):
    i = 0
    totalcharsarr = eliasc.eliasdec(encodedlist, 0)
    totalchars = totalcharsarr[1]
    i = i + totalcharsarr[0]
    # print("fdngfdjngndsgojnfg: " + str(i))
    next = 'a' # 'e', 'h'
    theascii = 0
    huffmancodel = 0
    thehcode = None
    charsf = 0


    """
    decoding the header
    to decode the header totalchars is the number of chars that have codes
    we get the ascii and the huffman code and build a table indexed by char that gives the huffman code
    the table is then used to construct a huffman tree that will be used in the decoding process
    """
    ctbl = [0] * 128
    while charsf < totalchars:
        if next == 'a':
            theascii = eliasc.base10(encodedlist, i, i + 7)
            # print("theascii: " + chr(theascii))
            # print(i)
            i = i + 7
            # print(i)
            next = 'e'
            continue
        elif next == 'e':
            huffmancodelarr = eliasc.eliasdec(encodedlist, i)
            huffmancodel = huffmancodelarr[1]
            # advance by length of elias code
            i = i + huffmancodelarr[0]
            # print(i)
            next = 'h'
            continue
        elif next == 'h':
            thehcode = encodedlist[i:i+huffmancodel]
            ctbl[theascii] = thehcode
            i = i + huffmancodel
            # print(i)
            next = 'a'
            charsf = charsf  + 1
            continue

    # print("codes")
    # print(ctbl[ord('a')])
    # print(ctbl[ord('_')])
    # print(ctbl[ord('r')])
    # print(ctbl[ord('y')])
    # print(ctbl[ord('b')])

    aroot = huffman.huffmantree(ctbl)
    print("huffman ready")
    # print("----------------------------------------------------------")
    # print(huffman.inorder(aroot))
    # print("----------------------------------------------------------")

    # print(i)


    """
    do the body
    1 or 0 can be used to check the type triplet or pair
    decode the bits to find the char offset or length 
    construct a string concurrently which is the decoded string
    
    """
    totalfieldsarr = eliasc.eliasdec(encodedlist, i)
    totalfields = totalfieldsarr[1]
    i = i + totalfieldsarr[0]
    astringarr = []
    ij = 0
    fieldsknown = 0
    # while i < len(encodedlist):
    numtrip = 0
    numchar = 0
    while fieldsknown < totalfields:
        # print("fiedsknown: " + str(fieldsknown) + " totalfields: " + str(totalfields))
        fieldsknown = fieldsknown + 1
        if (fieldsknown % 10000) == 0:
            print("fieldsknown: " + str(fieldsknown))
        # print("astringarr: " + str(astringarr))

        if encodedlist[i] == 1:
            i = i + 1
            getletterarr = huffman.getletter(encodedlist, aroot, i)
            astringarr = astringarr + [getletterarr[1]]
            i = i + getletterarr[0]
            ij = ij + 1
            # print("(0, " + getletterarr[1] +")")
            numchar = numchar + 1
        elif encodedlist[i] == 0:
            # astringarr = astringarr + astringarr[ ij -encodedlist[i][1]: ij-encodedlist[i][1] + encodedlist[i][2] ]
            # ij = ij + encodedlist[i][2]
            i = i  + 1
            encarr = eliasc.eliasdec(encodedlist, i)
            i = i + encarr[0]
            aoffset = encarr[1]
            encarr = eliasc.eliasdec(encodedlist, i)
            i = i + encarr[0]
            alength = encarr[1]
            for y in range(ij- aoffset, ij - aoffset + alength):
                astringarr = astringarr + [astringarr[y]]
            # astringarr = astringarr + astringarr[ ij - aoffset: ij-aoffset + alength ]
            ij = ij + alength
            # print("(" + str(aoffset) + ", " + str(alength) + ")")
            numtrip = numtrip + 1
    print("numchar: " + str(numchar) + " numtrip: "+ str(numtrip))
    return astringarr


"""
def bytestobitstring(abytearr):

    bitstring = []
    abyte = [0] * 8
    for i in range(0, len(abytearr)):
        thebyte = eliasc.base2(int(abytearr[i]))

        for j in range(0, len(thebyte)):
            abyte[7-j] = thebyte[len(thebyte) -j - 1]
        bitstring = bitstring + abyte
        abyte = [0] * 8
    return bitstring
"""
"""
converts bytearray elements to ints and then to array of 1 and 0 to produce an array for decoding 

"""
def bytestobitstring(abytearr):
    cache = [0]*256
    abyte = [0] * 8
    for i in range(0,256):
        thebyte = eliasc.base2(i)
        for j in range(0, len(thebyte)):
            abyte[7-j] = thebyte[len(thebyte) -j - 1]
        cache[i] = abyte
        abyte = [0] * 8
    bitstring = []

    for i in range(0, len(abytearr)):
        abyte = cache[int(abytearr[i])]
        bitstring = bitstring + abyte
    return bitstring


if __name__ == "__main__":
    binaryfilename = sys.argv[1]
    # atext = open(binaryfilename, 'rb').read();
    bytefile = open(binaryfilename, "rb");
    all = bytefile.read()
    # print(all)
    thestring = bytestobitstring(all)
    print("read file into memory")
    # print(thestring)
    astring = decoding(thestring)

    out = open("output_decoder_lzss.txt", 'w');
    for i in astring:
        print(i, end="", file=out)
    # out.write(astring)
    bytefile.close()
    out.close()



