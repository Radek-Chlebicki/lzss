import sys;
# Radek Chlebicki 29175224



import huffman
import eliasc
# how to convert z algorithm for lzss
# can we use ukkonen

# function that given the start of the window, window size , start of look ahead, look ahead size returns
# the lz77 tuple

"""
bvfgd
optimize task 1
miller rabin
"""


# for each stage when we need to do the z algorithm, this class
# helps to simulate the string lookahead + '$' window + lookahead

"""
This class creates a virtual representation of the string at the window and lookahead buffer
This basically works by taking the indeces of the start of the window and lookahead and the size
of those buffers. Then in the __getitem__ method it pretends there is a string such as 
lookahead+°+window+lookahead. But actually get item translates the index 0..lookaheadsize*2+windowsize+1
into an index that points to the original string and returns the letter there. 
This will be used in the z algo
"""
class virts:
    def __init__(self):
        self.astrptr = None
        self.windowsize = 0
        self.windowstart = 0
        self.lookaheadsize = 0
        self.lookaheadstart = 0

    def __len__(self):
        return self.windowsize + self.lookaheadsize + self.lookaheadsize + 1

    """
    translates the index to the actual position in the string 
    time O(1)
    space O(1) 
    """
    def __getitem__(self, item):
        if item < self.lookaheadsize:
            return self.astrptr[item + self.lookaheadstart];
        elif item == self.lookaheadsize:
            return '°'
        elif item < self.lookaheadsize + self.windowsize + 1:
            return self.astrptr[self.windowstart + item - self.lookaheadsize - 1]
        else:
            return self.astrptr[item + self.lookaheadstart - self.lookaheadsize - self.windowsize - 1];

astring = "abafuckabax"
virtstring = virts()
virtstring.astrptr  = astring
virtstring.windowsize = 7
virtstring.lookaheadsize = 4
virtstring.windowstart = 0
virtstring.lookaheadstart = 7


"""
this function takes an array of bits and converts it into a byte array
for every 8 bits it calculates an int and builds an array of ints
that array of ints is converted into a byte array
time O(n) 
space O(n) 
 
"""
def bitstringtobytearray(bitstring):
    power = 7
    vv = 0
    intstring = []
    for i in range(0, len(bitstring)):
        if bitstring[i] == 1:
            vv = vv + int(pow(2, power))
        power = power - 1;

        if i%8 == 7:
            power = 7
            intstring.append(vv)
            vv = 0

    i = i + 1
    power = 7
    intstring.append(vv)
    vv = 0

    return bytearray(intstring)

# astring1 = "aba"
# virtstring1 = virts()
# virtstring1.astrptr  = astring
# virtstring1.windowsize = 7
# virtstring1.lookaheadsize = 4
# virtstring1.windowstart = 0
# virtstring1.lookaheadstart = 7

# outstr = ""
# for i in range(0, len(virtstring)):
#     outstr = outstr + virtstring[i]
#
# print(len(virtstring))
# print(outstr)



# this returns the z array for a given string

"""
this is the z algorithm 
when we look at the zarray we are interested in all substrings matching the prefix of the lookahead
that begin inside the window. 

"""
def zalgo(avirt):
    zr = 0
    zl = 0
    i = 1
    zarray = [0] * len(avirt)

    while i < len(avirt):
        if i > zr :
            # print("case 1 ")
            j = 0
            interim = i
            while interim < len(avirt) and avirt[j] == avirt[interim]:
                j = j + 1
                interim = interim + 1
            zl = i
            zr = i + j - 1;
            zarray[i] = j

        else:
            if i + zarray[i - zl] < zr:
                # print("case 2 a")
                zarray[i] = zarray[i-zl]
            else:
                # print("case 2 b")
                zarray[i] = zr - i + 1
                interim = zr + 1
                j = zr - zl + 1
                cnt = 0
                while interim < len(avirt) and avirt[j] == avirt[interim]:
                    j = j + 1
                    interim = interim + 1
                    cnt = cnt + 1
                zarray[i] = zarray[i] + cnt

        i = i + 1


    return zarray

# print(zalgo(virtstring))
# print(zalgo("abaabaaba"))
# print(zalgo("aaaaaaxaaxy"))


"""
this builds the lzss encoding 
the function moves along the string. 
if the zalgorithm is able to match a pattern size 3 or greater, than the triplet (0, offset, length) is produced
the offset and the length are encoded using elias coding. The function then moves forward by the length amount. 
If the zalgorithm is only able to match a pattern 2 or less then the pair (1, char) is produced and the char
is encoded using huffman coding.

complexity: n is the number of characters in the text. w is window and l is the lookahead 
O(n(w+l))
traverse the n chars and do the zalgorithm at each char. 

"""

def encoding(astring, windowsize, lookaheadsize):




    # huffman
    ctbl = huffman.huffmanctbl(astring)
    print("made huffman")
    numberu = 0

    for i in range(0,128):
        if ctbl[i] != 0:
            numberu = numberu + 1
    """
    we make the table of huffman codes
    we find the number of different characters used in the input text
    we then build the header
    """
    header = []
    # add number of unique chars to header
    # print("numberu: " + str(numberu))

    header = header + eliasc.eliasenc(numberu)
    for i in range(0,128):
        if ctbl[i] != 0:
            # the ascii
            thebyte = eliasc.base2(i)
            abyte = [0] * 7
            for j in range(0, len(thebyte)):
                abyte[6 - j] = thebyte[len(thebyte) - j - 1]

            header = header + abyte
            # the length
            header = header + eliasc.eliasenc(len(ctbl[i]))
            # the huffman
            header = header + ctbl[i]


    print("made header")

    """
    here is where we start the actual encoding
    the product is an array of 0s and 1s 
    """
    lookaheadstart = 0
    windowstart = - windowsize
    virtstring = virts()
    virtstring.astrptr = astring
    encodedlist = []
    otherencodedlist = []

    fc = 0
    while lookaheadstart < len(astring):
        if lookaheadstart % 10000 == 0:
            print(lookaheadstart)
        if windowstart < 0:
            virtstring.windowstart = 0
            virtstring.windowsize = windowsize + windowstart
        else:
            virtstring.windowstart = windowstart
            virtstring.windowsize = windowsize

        if lookaheadstart + lookaheadsize -1 < len(astring):
            virtstring.lookaheadstart = lookaheadstart
            virtstring.lookaheadsize = lookaheadsize
        else:
            virtstring.lookaheadstart = lookaheadstart
            virtstring.lookaheadsize = len(astring) - lookaheadstart


        zarray = zalgo(virtstring)

        indexoflongest = 0;
        longest = 0


        # pattern only matters if it begins in the window
        # finds the longest substring
        for i in range(virtstring.lookaheadsize + 1, len(zarray)- virtstring.lookaheadsize):
            if zarray[i] >= longest:
                longest = zarray[i]
                indexoflongest = i


        # creating the lzss data
        if longest >= 3:
            encodedlist = encodedlist +  [0] + eliasc.eliasenc(virtstring.lookaheadstart - (virtstring.windowstart + indexoflongest-(virtstring.lookaheadsize+1))) + eliasc.eliasenc(longest)
            otherencodedlist = otherencodedlist +  [0] + [virtstring.lookaheadstart - (virtstring.windowstart + indexoflongest-(virtstring.lookaheadsize+1))] + [longest]
            windowstart = windowstart + longest
            lookaheadstart = lookaheadstart + longest
        else:
            encodedlist = encodedlist + [1] + ctbl[ord(astring[virtstring.lookaheadstart])]
            otherencodedlist = otherencodedlist + [1] + [astring[virtstring.lookaheadstart]]
            windowstart = windowstart + 1
            lookaheadstart = lookaheadstart + 1

        fc = fc + 1

    encodedlist = eliasc.eliasenc(fc) + encodedlist
    otherencodedlist = eliasc.eliasenc(fc) + ["."] +  otherencodedlist
    print(fc)
    print(eliasc.eliasenc(fc))
    # print("header: " + str(header))
    # print("encodedlist: " + str(encodedlist))
    # print("otherencodedlist: " + str(otherencodedlist))

    # print(header + encodedlist)
    to =  bitstringtobytearray(header +  encodedlist)
    # print(to)
    return to

# print("encoding --------------------------------------------------------------")
# print(encoding(astring, 7, 4))
# print(encoding("abababc", 3, 5))
# print(encoding("barrayar_bar_by_barrayar_bay", 15,15))


if __name__ == "__main__":
    textfilename = sys.argv[1]
    windowsize = int(sys.argv[2])
    print(windowsize)
    lookaheadsize = int(sys.argv[3])
    atext = open(textfilename, 'r', encoding="ascii",errors="ignore").read();
    bytesss = encoding(atext, windowsize, lookaheadsize)
    out = open("output_encoder_lzss.bin", 'wb');
    out.write(bytesss)
    out.close()

