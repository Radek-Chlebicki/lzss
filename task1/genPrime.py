import sys;
# Radek Chlebicki 29175224

import cProfile
import math
import random


"""
provides the base2 notation 
as an array of 1 and 0 
"""
def base2(x):
    binaryarr = []
    while x != 0:
        remainder = x % 2;
        binaryarr = [remainder] + binaryarr
        x = x // 2;

    return binaryarr


# print(base2(330))

"""
modular exponentiation using the repeated squaring algorithm 
"""
def repeatedSq(x,y,n):
    # print("start repeated")
    accumulator = x
    base2rep = base2(y)
    exp = 1
    for i in range (len(base2rep)-1, -1, -1):
        if base2rep[i] == 1:
           exp = exp * accumulator % n
        accumulator = accumulator * accumulator % n
    # print("stop repeated")
    return exp


# print(repeatedSq(10324210,741,323))
# print(pow(10324210,741,323))


"""
run with k = 64
finds the s and t then uses repeated squaring to perform the tests
when performing the tests a^(2^i * t) = (a^(2^(i-1) * t )^2
thus prev = (a^(2^(i-1) * t )
next = (a^(2^(i-1) * t )^2 % n 
"""
def millerRabinPrimalityTest(n, k):
    # print("start")

    if n%2 == 0:
        # print("stop")

        return False


    # n-1 = 2^s * t where t is odd
    s = 0
    t = n - 1
    # print("start while")
    while t%2 == 0:
        s = s + 1
        t = t/2
    # print("stop while")

    for i in range(0,k):
        a = random.randint(2, n-2)

        if (repeatedSq(a, n-1, n) !=1 ):
            # print("stop")

            return False


        prev = repeatedSq(a,t, n)
        for i in range(1, s+1):
            next = repeatedSq(prev,2,n)

            if next == 1 and prev != 1 and prev != n-1:
                # print("stop")

                return False
            prev = next
    # print("stop")

    return True


"""
the probability of choosing a non prime is z = range - num primes / range
range = (2^k -1) - 2^(k-1)
numprimes =  (2^k -1)/log2((2^k -1)) - 2^(k-1)/log2(2^(k-1)) 
after each try the cumulative probability of not drawing a prime is v
initially v = z and tries = 1 (after first draw)
loop
v = v * z  
tries = tries + 1
The number of tries should be such that v < 0.000001. 
"""


def generator(k):
    smaest = math.pow(2,k-1)
    # print("smaest: " + str(smaest))
    laest = math.pow(2,k) - 1
    # print("laest : " + str(laest))

    numberofprimes = laest/math.log2(laest) - smaest/math.log2(smaest)
    # print("numberofprimes: " + str(numberofprimes))
    rangesz = laest - smaest
    # print("range : " + str(rangesz))

    v = (rangesz -numberofprimes) / rangesz
    z = v
    numberoftries = 1
    # print("v: " + str(v))
    while v > 0.000001:
        # print(v)
        v = v * z
        numberoftries = numberoftries + 1

    # print("numberoftries: " + str(numberoftries))
    while numberoftries != 0:
        numberoftries = numberoftries - 1
        cr = random.randint(smaest, laest)
        # print(numberoftries)
        # print(cr)

        if millerRabinPrimalityTest(cr, 64):
            return cr

# print(generator(4))




if __name__ == "__main__":
    k = int(sys.argv[1])
    """
    write to stdout 
    """
    # print("hi")
    sys.stdout.write(str(generator(k)))
    sys.exit(0)

