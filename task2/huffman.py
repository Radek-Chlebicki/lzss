
import math


# Radek Chlebicki 29175224

class node:
    def __init__(self):
        self.left = None
        self.right = None
        self.f = 0
        self.letter = None

    def __str__(self):
        return "" + str(self.f) + "/" + str(self.letter)

    def __repr__(self):
        return "" + str(self.f) + "/" + str(self.letter)



"""
This is the implementation of the minheap
"""
class minheap:
    def __init__(self):
        self.heaparr = [0]

        # points to last item
        self.l = 0

    def __repr__(self):
        return str(self.heaparr[1:self.l+1])

    def left(self, i):
        return 2*i
    def right(self,i ):
        return 2*i +1
    def parent(self, i):
        return i // 2


    """
    complexity O(nlogn) 
    """
    def heapify(self, anodelist):
        for i in range(0, len(anodelist)):
            self.heaparr = self.heaparr + [anodelist[i]]
            self.l = i + 1
        for i in range(self.l // 2, 0, -1):
            self.sink(i)


    """
    time O(log(n))
    space O(1) 
    """
    def popmin(self):
        themin = self.heaparr[1]
        self.swap(1,self.l)
        self.l = self.l - 1;
        self.sink(1)
        return themin

    """
    time O(logn) 
    space O(1) 
    """
    def insert(self, x):
        if len(self.heaparr) - 1 == self.l:
            self.heaparr = self.heaparr + [x]
            self.l = self.l + 1
            self.swim(self.l)

        else:
            self.l = self.l + 1
            self.heaparr[self.l] = x
            self.swim(self.l)

    def swap(self, i, j):
        ati = self.heaparr[i]
        atj = self.heaparr[j]
        self.heaparr[i] = atj
        self.heaparr[j] = ati


    """
    time O(logn) 
    space O(1) 
    """
    def sink(self, i):
        if self.left(i) > self.l and self.right(i) > self.l:
            pass
        elif self.right(i) > self.l:
            if self.heaparr[i].f > self.heaparr[self.left(i)].f:
                self.swap(i, self.left(i))
                self.sink(self.left(i))
            else:
                pass

        elif self.heaparr[self.left(i)].f < self.heaparr[self.right(i)].f:
            if self.heaparr[i].f > self.heaparr[self.left(i)].f:
                self.swap(i, self.left(i))
                self.sink(self.left(i))
            else:
                pass
        else:
            if self.heaparr[i].f > self.heaparr[self.right(i)].f:
                self.swap(i, self.right(i))
                self.sink(self.right(i))
            else:
                pass

    """
    time O(logn) 
       space O(1) 
    """
    def swim(self, i):
        if self.parent(i) == 0:
            pass
        elif self.heaparr[i].f < self.heaparr[self.parent(i)].f:
            self.swap(self.parent(i), i)
            self.swim(self.parent(i))
        else:
            pass



"""
goes through a huffman tree and prints in order 

"""
def inorder(aroot):
    queue = []
    queue.append(aroot)
    while len(queue) > 0:
        cnode = queue.pop(0)
        print(cnode)
        if cnode.left != None:
            queue.append(cnode.left)
        if cnode.right != None:
            queue.append(cnode.right)


"""
populates a table with huffman codes
each code is available at the ascii index
given a tree
"""
def codetable(ctptr, aroot):
    stack = []
    stack.append([aroot, [] ])
    # inorder(aroot)
    while len(stack) > 0:
        cnode = stack.pop()
        if cnode[0].left != None:
            stack.append([cnode[0].left, cnode[1] + [0] ])
        if cnode[0].right != None:
            stack.append([cnode[0].right, cnode[1] + [1] ])
        if cnode[0].left == None and cnode[0].right == None:
            # print(cnode)
            ctptr[ord(cnode[0].letter)] = cnode[1]

"""
returns a code table
first it counts the occurance of each char in th string. 
then it creates nodes for each letter and its frequency 
it then heapifies them
then it pops the two nodes with the lowest frequencies and 
creates a new node the new node will be the parent of the two nodes removed
the new node is then inserted into the min heap 
This process continues until the minheap is empty. 

complexity 
time: O(nlogn)
"""
def huffmanctbl(astring):
    fcount = [0] * 128
    for i in astring:
        fcount[ord(i)] = fcount[ord(i)] + 1
    toaddnode = None
    anodelist = []
    numberofnodes = 0
    for i in range(0, len(fcount)):
        if fcount[i] != 0:
            toaddnode = node()
            toaddnode.f = fcount[i]
            toaddnode.letter = chr(i)
            anodelist = anodelist + [toaddnode]


    # check if there is only one node
    # if there is only one node then there is only 1 letter in alfabet
    # this means that we can just create the code and return.
    if len(anodelist) == 1:
        ctbl = [0]*128
        ctbl[ord(anodelist[0].letter)] = [0]
        return ctbl

    # toaddnode = node()
    # toaddnode.f = math.inf
    # toaddnode.letter = "root"
    # anodelist = anodelist + [toaddnode]
    minheapobj = minheap()
    minheapobj.heapify(anodelist)
    # print(minheapobj)

    smaller = None
    larger = None
    newnode = None
    while minheapobj.l > 0:
        # print("minheap: ", end="")
        # print(minheapobj, end=" ")
        # print("smaller: " + str(smaller), end=" ")
        # print("larger: " + str(larger), end=" ")
        # print("newnode: " + str(newnode))


        if minheapobj.l > 1:
            smaller = minheapobj.popmin()
            # print(minheapobj)
            # print(smaller)
            larger = minheapobj.popmin()
            # print(minheapobj)
            # print(larger)
            newnode = node()

            newnode.f = smaller.f + larger.f

            newnode.left = smaller
            newnode.right = larger
            newnode.letter = smaller.letter + larger.letter
            minheapobj.insert(newnode)
        else:
            aroot = minheapobj.popmin()

    ctbl = [0] * 128;
    codetable(ctbl, aroot)
    # print("codes")
    # print(ctbl[ord('a')])
    # print(ctbl[ord('_')])
    # print(ctbl[ord('r')])
    # print(ctbl[ord('y')])
    # print(ctbl[ord('b')])
    # print("codes" + str(len(ctbl)))
    #
    # for i in range(0, len(ctbl)):
    #     print(chr(i) + ": " + str(ctbl[i]))
    #
    # for i in range(0, len(ctbl)-1):
    #     if ctbl[i] == 0:
    #         continue
    #     for j in range(i+1, len(ctbl)):
    #         if ctbl[j] == 0:
    #             continue
    #         if len(ctbl[i]) >= len(ctbl[j]):
    #             shorter = ctbl[j]
    #             longer = ctbl[i]
    #         else:
    #             shorter = ctbl[i]
    #             longer = ctbl[j]
    #         for k in range(0, len(shorter)):
    #             if shorter[k] != longer[k]:
    #                 break
    #             if k == len(shorter) - 1:
    #                 print("IS PREFIX")
    #                 print(chr(i) + ": " + str(ctbl[i]))
    #                 print(chr(j) + ": " + str(ctbl[j]))

    return ctbl


"""
given a code table produces a huffman tree
This is used when the header is used to reconstruct the huffman codes. 
O(nlogn) 
"""
def huffmantree(ctblptr):
    aroot = node()
    for i in range(0,128):
        if ctblptr[i] != 0:
            cnode = aroot
            for j in range(0, len(ctblptr[i])):
                # print(cnode)
                if ctblptr[i][j] == 0:
                    if cnode.left != None:
                        cnode = cnode.left
                    else:
                        cnode.left = node()
                        cnode = cnode.left

                else:
                    if cnode.right != None:
                        cnode = cnode.right
                    else:
                        cnode.right = node()
                        cnode = cnode.right

            cnode.letter = chr(i)

    return aroot


"""
given a pointer into an array of 1s and 0s and the index where to start in that array as well as a huffman tree
gives you the letter corresponding to the huffman code and also the length of the code used so the decoder knows 
where to move next 
n is the length of the code. 
time: O(n) 
space: O(1)
"""
def getletter(astring, atree, si):
    # print("getletter")
    cnode = atree
    i = si
    while True:
        if cnode.left == None and cnode.right == None:
            return [i - si, cnode.letter]

        if astring[i] == 0:
            cnode = cnode.left
            i = i + 1
        elif astring[i] == 1:
            cnode = cnode.right
            i = i + 1


        # print("i " + str(i) + " si: " + str(si) + " i - si: " + str(i-si) + " the value: " +  str(astring[i]) )




# aroot = huffmantree(huffmanctbl("barrayar_bar_by_barrayar_bay"))
# print(getletter([1,1,1,1], aroot, 0))

# test = minheap();
#
#
#
# for i in range(3,7):
#     anode = node()
#     anode.f = i
#     test.heaparr = test.heaparr + [anode]
#     test.l = test.l + 1
#
# anode = node()
# anode.f = 1
# test.heaparr = test.heaparr + [anode]
# test.l = test.l + 1
#
# test.swim(test.l)
# print(test.heaparr)
#
#
#
#
#
# atest = minheap();
#
# anode = node()
# anode.f = 10
# atest.heaparr = atest.heaparr + [anode]
# atest.l = atest.l + 1
#
#
# for i in range(3,7):
#     anode = node()
#     anode.f = i
#     atest.heaparr = atest.heaparr + [anode]
#     atest.l = atest.l + 1
#
#
# atest.sink(1)
# print(atest.heaparr)