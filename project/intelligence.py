# This is a template.
# You should modify the functions below to match
# the signatures determined by the project specification
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def find_red_pixels(map_filename, upper_threshold=100, lower_threshold=50):
    """Finds all red pixels in the map"""
    picarray = mpimg.imread(map_filename)
    ylen = len(picarray)
    xlen = len(picarray[0])
    binArray = np.empty((ylen, xlen))
    for yval in range(0, ylen):
        for xval in range(0, xlen): #x and y loop to cover whole image
            pixel = picarray[yval, xval] * 255
            if pixel[0] > upper_threshold and pixel[1] < lower_threshold and pixel[2] < lower_threshold: #threshold for a red pixel
                binArray[yval, xval] = 1
            else:
                binArray[yval, xval] = 0
    plt.imsave('map-red-pixels.jpg', binArray, cmap='gray')
    return binArray

    # two for loops, check rgb value, then add to 2d numpy array


def find_cyan_pixels(map_filename, upper_threshold=100, lower_threshold=50):
    """Finds all cyan pixels in the map"""
    picarray = mpimg.imread(map_filename)
    ylen = len(picarray)
    xlen = len(picarray[0])
    binArray = np.empty((ylen, xlen))
    for yval in range(0, ylen):
        for xval in range(0, xlen): #x and y loop to cover whole image
            pixel = picarray[yval, xval] * 255
            if pixel[0] < upper_threshold and pixel[1] > lower_threshold and pixel[2] > lower_threshold: #threshold for a cyan pixel
                binArray[yval, xval] = 1
            else:
                binArray[yval, xval] = 0
    plt.imsave('map-cyan-pixels.jpg', binArray, cmap='gray')
    return binArray


class Queue:
    """A class which is a queue, and has functions to add and remove values"""
    def __init__(self):
        self.queue = np.ndarray([], dtype=int) #creates queue

    def addVal(self, newVal):
        self.queue = np.append(self.queue, newVal) #adds a value to the queue

    def removeVal(self):
        if self.queue.size < 1: #checks queue isnt empty
            return
        item = self.queue[1]
        self.queue = np.delete(self.queue, 1)  #pops item from queue
        return item


def eight_neighbour(pixelx, pixely, array):
    """Finds all eight neighbours which are a pavement pixel"""
    neighbours = []
    for x in range(0, 3):
        for y in range(0, 3): #this will loop around a 3x3 grid
            ycoord = (pixely - 1 + y)
            xcoord = (pixelx - 1 + x)
            if xcoord < 1053 and ycoord < 1140:
                newpixel = array[ycoord, xcoord]
                if newpixel == 1:
                    if y != 1 or x != 1: #make sure we ignore the middle of the 3x3 grid
                        neighbours.append((ycoord, xcoord))
    return neighbours


def detect_connected_components(IMG):
    """Generates a list of all connected components in the image"""
    # To improve the algorithm, I added a counter to add the lenghth of each connected component to an array which I then put into a text file.
    ccsize = 0
    picarray = IMG
    ylen = len(picarray)
    xlen = len(picarray[0])
    MARK = np.empty((ylen, xlen))
    Q = Queue()
    cclist = []
    for yval in range(0, ylen):
        for xval in range(0, xlen):
            pixel = picarray[yval, xval]
            if pixel == 1 and MARK[yval, xval] == 0:
                MARK[yval, xval] = 1
                Q.addVal((yval, xval))
                ccsize = 0
                while Q.queue.size > 1:
                    q = (Q.removeVal(), Q.removeVal())
                    ccsize += 1 #generated the size of the cc
                    allneighbours = eight_neighbour(q[1], q[0], picarray)
                    for item in allneighbours:
                        if MARK[item] == 0:
                            MARK[item] = 1
                            Q.addVal(item)
                cclist.append(ccsize) #adds the size of the cc to a list of sizes of cc's
    f = open("cc-output-2a.txt", "w")
    z = 1
    for c in cclist:
        f.write("Connected Component {}, number of pixels = {}".format(z, c))
        f.write("\n")
        z += 1
    f.write("Total number of connected components = {}".format(len(cclist)))
    return MARK


def bubble_sort(list):
    """Does a bubble sort on a list of tuples"""
    listlen = len(list)
    for i in range(listlen - 1):
        f = 0
        for j in range(listlen - 1):
            if list[j][1] > list[j+1][1]:
                x = list[j]
                list[j] = list[j+1]
                list[j+1] = x
                f = 1
        if f == 0:
            break
    list.reverse()
    return list


def detect_connected_components_sorted(markarray):
    """Generates MARK again, and also a list of connected components, and this time keeps track of the highest two connected components on the way. It then orders all the 
    connected components and writes it to a file. It then produces an image of the two highest connected components."""
    ccsize = 0
    ccnumber = 0
    picarray = markarray
    ylen = len(picarray)
    xlen = len(picarray[0])
    currentcc = []
    MARK2 = np.empty((ylen, xlen))
    TOP2CC = np.empty((ylen, xlen))
    Q = Queue()
    cclist = []
    firstcc = []
    secondcc = []
    for yval in range(0, ylen):
        for xval in range(0, xlen):
            pixel = picarray[yval, xval]
            if pixel == 1 and MARK2[yval, xval] == 0:
                MARK2[yval, xval] = 1
                currentcc.append((yval, xval))
                Q.addVal((yval, xval))
                ccsize = 0
                ccnumber += 1
                while Q.queue.size > 1:
                    q = (Q.removeVal(), Q.removeVal())
                    ccsize += 1
                    allneighbours = eight_neighbour(q[1], q[0], picarray)
                    for item in allneighbours:
                        if MARK2[item] == 0:
                            MARK2[item] = 1
                            Q.addVal(item)
                            currentcc.append(item)
                cclist.append((ccnumber, ccsize))
                if len(currentcc) > len(secondcc): #This checks if the size of the current cc is biggest than the two saved highest ones
                    secondcc = currentcc[:]
                    if len(currentcc) > len(firstcc):
                        secondcc = firstcc[:]
                        firstcc = currentcc[:]
                currentcc.clear()
    for p in firstcc:
        TOP2CC[p] = 1 
    for p in secondcc:
        TOP2CC[p] = 1 #these two for loops create a 2d array with same dimensions as mark, with only the two largest connected components on them
    f = open("cc-output-2b.txt", "w")
    z = 1
    orderedcclist = bubble_sort(cclist)
    for c in orderedcclist:
        f.write(
            "Connected Component {}, number of pixels = {}".format(c[0], c[1]))
        f.write("\n")
        z += 1
    f.write("Total number of connected components = {}".format(ccnumber))
    plt.imsave('cc-top-2.jpg', TOP2CC, cmap='gray')
