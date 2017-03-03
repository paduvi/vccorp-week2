#!/usr/bin/env python

import numpy as np
from scipy.misc import imread, imsave
import matplotlib.pyplot as plt
import click


def initial_random_centroid(k):
    return np.random.randint(256, size=(k, 3))


def get_cluster(centroids, pixels):
    return np.asarray([np.argmin(distance(centroids, pixel)) for pixel in pixels])


def distance(p1, p2):
    return np.linalg.norm(p1 - p2, axis=1)


@click.command()
@click.argument('k', default=192)
@click.argument('inp', default='input.jpg')
@click.argument('out', default='output.jpg')
def compressor(k, inp, out):
    original_img = imread(inp)
    height, width, dim = original_img.shape
    picture_vector = np.reshape(original_img, (height * width, dim))

    centroids = initial_random_centroid(k)
    flag = False
    loop = 0

    while not flag:
        temp = centroids.copy()
        clusters = get_cluster(centroids=centroids, pixels=picture_vector)
        for i in range(k):
            neighbors = picture_vector[clusters == i]
            if neighbors.size != 0:
                centroids[i] = np.mean(neighbors, axis=0)
        flag = (temp == centroids).all()
        loop += 1
        print 'Loop: ', loop

    new_picture_vector = np.asarray([centroids[cluster] for cluster in clusters])
    new_img = np.uint8(np.reshape(new_picture_vector, (height, width, dim)))

    # Show the original image
    plt.subplot(1, 2, 1)
    plt.imshow(original_img)
    plt.title('Before')

    # Show the tinted image
    plt.subplot(1, 2, 2)

    # A slight gotcha with imshow is that it might give strange results
    # if presented with data that is not uint8. To work around this, we
    # explicitly cast the image to uint8 before displaying it.
    imsave(out, new_img)
    plt.imshow(new_img)
    plt.title('After (k={0})'.format(k))
    plt.show()


if __name__ == '__main__':
    compressor()
