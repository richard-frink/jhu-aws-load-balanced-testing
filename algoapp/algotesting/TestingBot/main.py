from skimage import color
from scipy.misc import imsave
import os
import numpy as np
from testingapp.algotesting.TestingBot.Sorter import Sorter as sort

args = "bubble"

img = np.zeros((200, 200, 3), dtype='float32') # hsv works in range from 0 - 1

for i in range(img.shape[1]):
    img[:,i,:] = i / img.shape[0], .9, .9

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

    if len(newMoves) > maxMoves:
        maxMoves = len(newMoves)
    moves.append(newMoves)

currentMove = 0

def swap_pixels(row, places):
    tmp = img[row,places[0],:].copy()
    img[row,places[0],:] = img[row, places[1], :]
    img[row,places[1],:] = tmp

# 24 fps, and we want a 5 second gif 24 * 5 = 120 total frames (* 24 5)
movie_image_step = maxMoves // 120
movie_image_frame = 0

os.makedirs(args.sorter, exist_ok=True)

while currentMove < maxMoves:
    for i in range(img.shape[0]):
        if currentMove < len(moves[i]) - 1:
            swap_pixels(i, moves[i][currentMove])

    if currentMove % movie_image_step == 0:
        imsave('%s/%05d.png' % (args, movie_image_frame), color.convert_colorspace(img, 'HSV', 'RGB'))
        movie_image_frame += 1
    currentMove += 1

if __name__ == '__main__':
    print("okjsdnv")

