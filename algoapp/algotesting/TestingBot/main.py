from skimage import color
from scipy.misc import imsave
import os
import numpy as np
import math

img = np.zeros((200, 200, 3), dtype='float32')  # hsv works in range from 0 - 1

class Sorter:
    def bubblesort(self, test):
        swaps = []
        for i in range(len(test)):
            for k in range(len(test) - 1, i, -1):
                if (test[k] < test[k - 1]):
                    swaps.append([k, k - 1])
                    tmp = test[k]
                    test[k] = test[k - 1]
                    test[k - 1] = tmp
        return test, swaps

    def merge(self, lefthalf, righthalf):
        res = []
        while len(lefthalf) != 0 and len(righthalf) != 0:
            if lefthalf[0] < righthalf[0]:
                res.append(lefthalf[0])
                lefthalf.remove(lefthalf[0])
            else:
                res.append(righthalf[0])
                righthalf.remove(righthalf[0])
        if len(lefthalf) == 0:
            res = res + righthalf
        else:
            res = res + lefthalf
        return res

    def mergesort(self, test):
        unsortedlist = test
        if len(unsortedlist) <= 1:
            return unsortedlist
        middle = len(unsortedlist) // 2
        leftlist = unsortedlist[:middle]
        rightlist = unsortedlist[middle:]

        leftlist = self.mergesort(leftlist)
        rightlist = self.mergesort(rightlist)
        return self.merge(leftlist, rightlist)

    def insertionsort(self, test):
        inputlist = test
        for i in range(1, len(inputlist)):
            j = i - 1
            nextelement = inputlist[i]
            while (inputlist[j] > nextelement) and (j >= 0):
                inputlist[j + 1] = inputlist[j]
                j = j - 1
            inputlist[j + 1] = nextelement
        return inputlist

    def shellsort(self, test):
        inputlist = test
        gap = math.floor(len(inputlist) / 2)
        while gap > 0:
            for i in range(gap, len(inputlist)):
                temp = inputlist[i]
                j = i
                while j >= gap and inputlist[j - gap] > temp:
                    inputlist[j] = inputlist[j - gap]
                    j = j - gap
                inputlist[j] = temp
            gap = math.floor(gap / 2)
        return inputlist

    def moveDown(self, aList, first, last):
        global swaps
        largest = 2 * first + 1
        while largest <= last:
            if (largest < last) and (aList[largest] < aList[largest + 1]):
                largest += 1

            if aList[largest] > aList[first]:
                swaps.append([largest, first])
                self.swap(aList, largest, first)
                first = largest;
                largest = 2 * first + 1
            else:
                return  # force exit

    def swap(self, A, x, y):
        tmp = A[x]
        A[x] = A[y]
        A[y] = tmp

    def heapsort(self, aList):
        global swaps
        swaps = []
        length = len(aList) - 1
        leastParent = length // 2
        for i in range(leastParent, -1, -1):
            self.moveDown(aList, i, length)

        for i in range(length, 0, -1):
            if aList[0] > aList[i]:
                swaps.append([0, i])
                self.swap(aList, 0, i)
                self.moveDown(aList, 0, i - 1)
        return aList, swaps


def swap_pixels(row, places):
    tmp = img[row,places[0],:].copy()
    img[row,places[0],:] = img[row, places[1], :]
    img[row,places[1],:] = tmp


def sort(selection):
    sort = Sorter()
    args = selection

    for i in range(img.shape[1]):
        img[:, i, :] = i / img.shape[0], .9, .9

    in_rgb = color.convert_colorspace(img, 'HSV', 'RGB')

    # Uncomment bellow to see starting image
    imsave('initial.png', in_rgb)

    for i in range(img.shape[0]):
        np.random.shuffle(img[i, :, :])

    in_rgb = color.convert_colorspace(img, 'HSV', 'RGB')
    imsave('initial_shuffled.png', in_rgb)

    # we've now got our shuffled, perfect image. let's jump through hoops now

    maxMoves = 0
    moves = []

    for i in range(img.shape[0]):
        newMoves = []
        if args == 'bubble':
            _, newMoves = sort.bubblesort(list(img[i, :, 0]))
        elif args == 'quick':
            _, newMoves = sort.quicksort(list(img[i, :, 0]))
        elif args == 'heap':
            # need to convert to integers for heap
            integer_version = img[i, :, 0] * 10000
            integer_version = integer_version.astype(int)
            _, newMoves = sort.heapsort(list(integer_version))
        elif args == 'heap':
            # need to convert to integers for heap
            integer_version = img[i, :, 0] * 10000
            integer_version = integer_version.astype(int)
            _, newMoves = sort.heapsort(list(integer_version))
        elif args == 'heap':
            # need to convert to integers for heap
            integer_version = img[i, :, 0] * 10000
            integer_version = integer_version.astype(int)
            _, newMoves = sort.heapsort(list(integer_version))

        if len(newMoves) > maxMoves:
            maxMoves = len(newMoves)
        moves.append(newMoves)

    currentMove = 0

    # 24 fps, and we want a 5 second gif 24 * 5 = 120 total frames (* 24 5)
    movie_image_step = maxMoves // 540
    movie_image_frame = 0

    os.makedirs(args, exist_ok=True)

    while currentMove < maxMoves:
        for i in range(img.shape[0]):
            if currentMove < len(moves[i]) - 1:
                swap_pixels(i, moves[i][currentMove])

        if currentMove % movie_image_step == 0:
            imsave('%s/%05d.png' % (args, movie_image_frame), color.convert_colorspace(img, 'HSV', 'RGB'))
            movie_image_frame += 1
        currentMove += 1


if __name__ == '__main__':
    # read input
    # run sort based off input
    # create video
    # show video when finished
    sort("heap")
    # have different endpoints for every environment, no need to get crazy
    # ex - one sorting algo per server
    #    only thing different per environment will be the button they can press
    #    aka the sorting method displayed
