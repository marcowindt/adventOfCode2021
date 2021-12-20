import os
import numpy as np


KERNEL = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),   (0, 0),  (0, 1),
    (1, -1),   (1, 0),  (1, 1)
]


def enhance(img, algorithm):
    image_height = img.shape[0]
    image_width = img.shape[1]

    image_conv = np.zeros(img.shape)

    for i in range(1, image_height - 1):
        for j in range(1, image_width - 1):
            lookup = int(''.join(str(int(x)) for x in [img[i + dx, j + dy] for dx, dy in KERNEL]), 2)
            image_conv[i, j] = algorithm[lookup]

    image_conv[0] = np.array([image_conv[1, 1] for _ in range(image_width)])
    image_conv[-1] = np.array([image_conv[1, 1] for _ in range(image_width)])
    image_conv[:, 0] = np.array([image_conv[1, 1] for _ in range(image_height)])
    image_conv[:, -1] = np.array([image_conv[1, 1] for _ in range(image_height)])
    image_conv = np.pad(image_conv, 1, mode='constant', constant_values=image_conv[0, 0])

    return image_conv


def print_image(img):
    for i in range(img.shape[0]):
        row = ''
        for j in range(img.shape[1]):
            if img[i, j]:
                row += '#'
            else:
                row += '.'
        print(row)


def solution():
    with open(os.path.join(os.path.dirname(__file__), './input.txt'), 'r') as fd:
        enhancement_image = fd.read()

    algorithm, input_image = enhancement_image.split('\n\n')
    algorithm = np.array([1 if pixel == '#' else 0 for pixel in algorithm])

    input_image = input_image.split('\n')
    original_image = []
    for input_row in input_image:
        row = []
        for pixel in input_row:
            if pixel == '#':
                row.append(1)
            else:
                row.append(0)
        original_image.append(row)

    image = np.array(original_image)
    image = np.pad(image, 3, mode='constant', constant_values=0)

    for _ in range(2):
        image = enhance(image, algorithm)
    # print_image(image)

    print("PART 1:", int(np.sum(np.sum(image))))

    for _ in range(48):
        image = enhance(image, algorithm)

    print("PART 2:", int(np.sum(np.sum(image))))


if __name__ == '__main__':
    solution()

"""
.........
.........
...#.#...
....##...
...#.#...
.........
.........
.........
"""
