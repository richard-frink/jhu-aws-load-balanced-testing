from skimage import color
from scipy.misc import imsave
import os
import glob
from os import listdir
from os.path import isfile, join
import numpy as np
import math
from cv2 import VideoWriter, VideoWriter_fourcc, imread, resize

from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route("/")
def home():
    return render_template("index.html")

img = np.zeros((200, 200, 3), dtype='float32')  # hsv works in range from 0 - 1

class Sorter:
    def bubblesort(self, lst):
        swaps = []
        for i in range(len(lst)):
            for k in range(len(lst) - 1, i, -1):
                if (lst[k] < lst[k - 1]):
                    swaps.append([k, k - 1])
                    tmp = lst[k]
                    lst[k] = lst[k - 1]
                    lst[k - 1] = tmp
        return lst, swaps

    def insertionsort(self, lst):
        swaps = []
        for i in range(1, len(lst)):
            j = i - 1
            nextelement = lst[i]
            while (lst[j] > nextelement) and (j >= 0):
                swaps.append([j + 1, j])
                lst[j + 1] = lst[j]
                j = j - 1
            lst[j + 1] = nextelement
        return lst, swaps

    def shellsort(self, lst):
        gap = math.floor(len(lst) / 2)
        swaps = []
        while gap > 0:
            for i in range(gap, len(lst)):
                temp = lst[i]
                j = i
                while j >= gap and lst[j - gap] > temp:
                    swaps.append([j, j - gap])
                    lst[j] = lst[j - gap]
                    j = j - gap
                lst[j] = temp
            gap = math.floor(gap / 2)
        return lst, swaps

    def moveDown(self, lst, first, last):
        global heapswaps
        largest = 2 * first + 1
        while largest <= last:
            if (largest < last) and (lst[largest] < lst[largest + 1]):
                largest += 1

            if lst[largest] > lst[first]:
                heapswaps.append([largest, first])
                self.swap(lst, largest, first)
                first = largest
                largest = 2 * first + 1
            else:
                return  # force exit

    def swap(self, A, x, y):
        tmp = A[x]
        A[x] = A[y]
        A[y] = tmp

    def heapsort(self, lst):
        global heapswaps
        heapswaps = []
        length = len(lst) - 1
        leastParent = length // 2
        for i in range(leastParent, -1, -1):
            self.moveDown(lst, i, length)

        for i in range(length, 0, -1):
            if lst[0] > lst[i]:
                heapswaps.append([0, i])
                self.swap(lst, 0, i)
                self.moveDown(lst, 0, i - 1)
        return lst, heapswaps


def swap_pixels(row, places):
    tmp = img[row, places[0], :].copy()
    img[row, places[0], :] = img[row, places[1], :]
    img[row, places[1], :] = tmp


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
        elif args == 'insertion':
            _, newMoves = sort.insertionsort(list(img[i, :, 0]))
        elif args == 'shell':
            _, newMoves = sort.shellsort(list(img[i, :, 0]))
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

def makevideo(images, algo, outimg, fps=24, size=None,
               is_color=True, format="mp4v"):

    fourcc = VideoWriter_fourcc(*format)
    vid = None
    for image in images:
        if not os.path.exists(image):
            raise FileNotFoundError(image)
        img = imread(image)
        if vid is None:
            if size is None:
                size = img.shape[1], img.shape[0]
            vid = VideoWriter(algo+"/"+outimg, fourcc, float(fps), size, is_color)
        if size[0] != img.shape[1] and size[1] != img.shape[0]:
            img = resize(img, size)
        vid.write(img)
    vid.release()
    return vid

def clearalgo(algo):
    files = glob.glob(algo+"/*")
    for f in files:
        os.remove(f)

if __name__ == '__main__':
    # sort("bubble")
    # sort("insertion")
    # sort("shell")
    # sort("heap")
    # have different endpoints
    # read input
    # run sort based off input
    # create video
    algos = ["bubble", "insertion", "shell", "heap"]
    for algo in algos:
        clearalgo(algo)

    algo = "insertion"
    sort(algo)
    images = [algo+"/"+f for f in listdir(algo) if isfile(join(algo, f))]
    vid = makevideo(images, algo, algo+".mp4")

    app.run(debug=True)

    # show video when finished for every environment, no need to get crazy
    # ex - one sorting algo per server
    #    only thing different per environment will be the button they can press
    #    aka the sorting method displayed
