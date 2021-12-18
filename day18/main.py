import os
from collections import Counter
from queue import PriorityQueue
from math import ceil


EXAMPLE = """[[[[4,3],4],4],[7,[[8,4],9]]]"""
EXAMPLE_MAGNITUDE = """[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"""
LARGER_EXAMPLE = """[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]"""
HOMEWORK = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""


class Val:

    def __init__(self, val, parent=None):
        self.parent = parent
        self.val = val

    def __str__(self):
        return "{}".format(self.val)


class Node:

    def __init__(self, parent=None, left=None, right=None):
        self.parent = parent
        self.left = left
        self.right = right

    def __str__(self):
        return "[{},{}]".format(self.left, self.right)


def make_tree(fish, parent=None):
    if isinstance(fish, list):
        left, right = fish
        n = Node(parent=parent)
        n.left = make_tree(left, parent=n)
        n.right = make_tree(right, parent=n)
        return n
    else:
        return Val(val=fish, parent=parent)


def add(left, right):
    n = Node(left=left, right=right)
    n.left.parent = n
    n.right.parent = n
    return n


def magnitude(fish):
    if isinstance(fish, Node):
        return 3 * magnitude(fish.left) + 2 * magnitude(fish.right)
    else:
        return fish.val


def explode(snail, depth=0):
    if isinstance(snail, Val):
        return False

    if depth >= 4:
        # we are going to nuke this %#@$*
        # if not isinstance(snail.left, Val):
        #     return explode(snail.left, depth=depth + 1)
        # if not isinstance(snail.right, Val):
        #     return explode(snail.right, depth=depth + 1)
        if snail.parent.left == snail:
            # explode left leaf
            current_node = snail.parent

            while current_node.parent is not None and current_node == current_node.parent.left:
                current_node = current_node.parent

            if current_node.parent is None:
                current_node = None
            else:
                current_node = current_node.parent

            if current_node is None:
                snail.left.val = 0
            else:
                current_node = current_node.left
                while isinstance(current_node, Node):
                    current_node = current_node.right
                current_node.val += snail.left.val

            # explode right leaf
            current_node = snail.parent.right
            while isinstance(current_node, Node):
                current_node = current_node.left
            current_node.val += snail.right.val

            exploded = Val(0, parent=snail.parent)
            snail.parent.left = exploded

        elif snail.parent.right == snail:
            # explode right leaf
            current_node = snail.parent

            while current_node.parent is not None and current_node == current_node.parent.right:
                current_node = current_node.parent

            if current_node.parent is None:
                current_node = None
            else:
                current_node = current_node.parent

            if current_node is None:
                snail.right.val = 0
            else:
                current_node = current_node.right
                while isinstance(current_node, Node):
                    current_node = current_node.left
                current_node.val += snail.right.val

            # explode left leaf
            current_node = snail.parent.left
            while isinstance(current_node, Node):
                current_node = current_node.right
            current_node.val += snail.left.val

            exploded = Val(0, parent=snail.parent)
            snail.parent.right = exploded
        else:
            print('OH NOOOO!')
        return True
    else:
        return explode(snail.left, depth=depth + 1) or explode(snail.right, depth=depth + 1)


def split(snail):
    if isinstance(snail, Val):
        if snail.val >= 10:
            n = Node(parent=snail.parent)
            n.left = Val(val=snail.val // 2, parent=n)
            n.right = Val(val=ceil(snail.val / 2), parent=n)

            if snail.parent.left == snail:
                snail.parent.left = n
            elif snail.parent.right == snail:
                snail.parent.right = n
            else:
                print('OH NO!')
            return True
        return False
    return split(snail.left) or split(snail.right)


def reduce(snail: Node):
    while explode(snail) or split(snail):
        continue


def solution():
    with open(os.path.join(os.path.dirname(__file__), './input.txt'), 'r') as fd:
        snails = fd.read()

    # snails = HOMEWORK
    fish = [eval(snail) for snail in snails.split('\n')]

    snail = make_tree(fish[0])
    for i in range(1, len(fish)):
        snail = add(snail, make_tree(fish[i]))
        reduce(snail)

    print("PART 1:", magnitude(snail))

    m = 0
    for snail_x in fish:
        for snail_y in fish:
            if snail_x == snail_y:
                continue
            snail = make_tree([snail_x, snail_y])
            reduce(snail)
            mag = magnitude(snail)
            if mag > m:
                m = mag

    print("PART 2:", m)


if __name__ == '__main__':
    solution()


#  [1, 2]
#  /    \
# 1      2
#
#     [ [1, 2], 3 ]
#       /       \
#     [1, 2]     3
#      /  \
#     1    2
#
#     [ 9, [8, 7] ]
#      /       \
#     9       [8, 7]
#             /    \
#            8      7
#
#     [ [1, 9], [8, 5] ]
#         /        \
#      [1, 9]      [8, 5]
#       /   \      /    \
#      1     9    8      5
#
#       [ [ [ [0, 7], 4], [ [7, 8], [0, [6, 7] ] ] ], [1, 1] ]
#                              /                           \
#   [ [ [0, 7], 4], [ [7, 8], [0, [6, 7] ] ] ]              [1, 1]
#                /                   \                      /    \
#        [ [0, 7], 4]           [ [7, 8], [0, [6, 7] ] ]   1      1
#              /     \                 /      \
#          [0, 7]     4             [7, 8]     [0, [6, 7] ]
#            /  \                   /   \       /       \
#           0    7                 7     8     0        [6, 7]
#                                                        /  \
#                                                       6    7
#
#         [ [ [ [0, 7], 4], [7, [ [8, 4], 9] ] ], [1, 1] ]
#                            /                        \
#         [ [ [0, 7], 4], [7, [ [8, 4], 9] ] ]       [1, 1]
#                 /             \                    /    \
#         [ [0, 7], 4]        [7, [ [8, 4], 9] ]    1      1
#            /      \          /         \
#         [0, 7]     4        7       [ [8, 4], 9]
#         /    \                       /        \
#        0      7                   [8, 4]       9
#                                   /    \
#                                  8      4
