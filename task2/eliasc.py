import math




# Radek Chlebicki 29175224


"""
find the base2 representation of a number 
"""
def base2(x):
    binaryarr = []
    while x != 0:
        r = x % 2;
        binaryarr = [r] + binaryarr
        x = x // 2;

    return binaryarr

# print(base10to2(0))
"""
convert the base2 representation back to a number
this is designed to work on an existing array
"""
def base10(binarryarr, si, ei):
    base10 = 0
    for i in range(si, ei):
        # print(base10)
        base10 = base10 + int(binarryarr[i]) * math.pow(2, (ei-si) - 1 - i + si)
    return int(base10)

# print("111: " + str(base2to10(['1', '1', '1'], 1 , 3)))

"""
given a number produce 
an array of 0s and 1s which
 represents the elias encoding of a number 
"""
def eliasenc(x):
    # print("enc")
    n = base2(x)
    # length of the minimal code
    l = len(n)
    # lenght of the elias code
    codel = 0;
    # copy of l
    lc = l
    # find the length of the final elias code
    while lc > 1:
        codel = lc + codel
        lc = math.ceil(math.log2(lc))

    # the very first item
    codel = codel + 1
    # print(codel)
    #
    eout = [0] * codel
    k = 0
    while l > 0:
        # this is what we are copying in right now
        codel = codel - l

        for i in range(0,l):
            # print("codel: "+ str(codel))

            eout[codel + i] = n[i]
        # this is the new length
        # print(len(n))
        n = base2(l - 1)
        if len(n) != 0:
            n[0] = 0
        l = len(n)
    return eout


# print(eliasenc(561))
# for i in range(0,11):
#     print(str(i) + ": " + str(eliasenc(i)))


"""
given a large array of 0s and 1s and an index to start at 
return the number encoded and the length of encoding so that the lzss decoder
knows where to continue
"""
def eliasdec(encarr, si):
    length = 1
    i = si;

    while encarr[i] == 0:
        encarr[i] = 1
        oldle = length
        length = base10(encarr, i, i + length) + 1
        # print(length)
        i = i + oldle

    # print("i + length: " + str(i + length))

    return [i + length - si , base10(encarr, i, i + length)]

print(eliasenc(561))
print(eliasdec(eliasenc(561), 0))