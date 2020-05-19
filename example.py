#!/usr/bin/env python3

from libgroups import Group, visibleToInternal

# You can create a group instance from a Cayley table and the set of elements.
# Make sure to use visibleToInternal if your Cayley table is in the form [row][column].
cayleyTable = [
    ["u", "v", "w", "x", "y", "z"],
    ["v", "u", "y", "z", "w", "x"],
    ["w", "z", "u", "y", "x", "v"],
    ["x", "y", "z", "u", "v", "w"],
    ["y", "x", "v", "w", "z", "u"],
    ["z", "w", "x", "v", "u", "y"],
]
group1 = Group.fromCayleyTable(["u", "v", "w", "x", "y", "z"], visibleToInternal(cayleyTable))

print("Group 1")
print(group1)


# Alternatively, provide an operation function and a group of elements with which the operation
# can be used.
def operation(a, b):
    return (a * b) % 9

elements = [1, 2, 4, 5, 7, 8]

group2 = Group.fromOperation(elements, operation)

print("\n\nGroup 2")
print(group2)


# Using libpermutations, you can create a group from a set of permutations.
# The permutations should be in the form of the second row of a 2-row permutation matrix:
#
#  e.g.      [ 0  1  2  3 ]
#            [ 1  0  3  2 ]  <--- this one
#
# You must always use consecutive numbers starting at 0.
# The below example is the symmetries of a square, where { l, m, n, o } are reflections,
# and { s, t, u, e } rotations.

from libpermutations import generateGroup

elements = ["l", "m", "n", "o", "s", "t", "u", "e"]

permutations = [
    [3, 2, 1, 0],   # l
    [0, 3, 2, 1],   # m
    [1, 0, 3, 2],   # n
    [2, 1, 0, 3],   # o
    [3, 0, 1, 2],   # s
    [2, 3, 0, 1],   # t
    [1, 2, 3, 0],   # u
    [0, 1, 2, 3],   # e
]

mygroup3 = generateGroup(elements, permutations)

print("\n\nGroup 3")
print(mygroup3)


# Using the `Element` class, you can generate Cayley tables from operations that don't give exact
# values, and also use shorthand for elements.
# In this example we define six matrices using our `Element`-derived `Matrix` class, and form a Cayley table
# under matrix multiplication (implemented by numpy).
#
# The `Element` class has two attributes
#   `name`: an identifier for the element, which will be how it is shown in Cayley tables and other output
#   `value`: the value of the element - this can be anything
#
# If your value type does not have the `-` operator defined for it in such a way that
# gives an int or float result, you need to implement `isApproxEq` on your class yourself. It should take two arguments:
#   `b`: the other element to compare against of the same type as self
#   `approximation`: the value below which the elements will be considered equal
# It should return True when self and b are approximately equal, otherwise False.
# 
# The libgroups function `formCayleyTable` takes a list of elements and an operation like `Group.fromOperation`, but also takes
# the approximation argument. This has the same function as described above. The difference between the two is that `fromOperation`
# makes an exact comparison between the result of the operation and elements provided, whereas `formCayleyTable` uses approximation
# to do this comparison. This is great for groups involving surds/irrational numbers.
# The list of elements passed to `formCayleyTable` must be instances of an `Element`-derived class.

from libgroups import Element, formCayleyTable
import numpy as np
from math import sqrt as rt

class Matrix(Element):
    def isApproxEq(self, b, approximation):
        for r in range(len(self.value)):
            for c in range(len(self.value[r])):
                if abs(b.value[r][c] - self.value[r][c]) > approximation:
                    return False
        return True

def operation(a, b):
    return Matrix("NONAME", np.matmul(a.value, b.value))

elements = [
    Matrix("P", np.array([
        [1, 0],
        [0, 1]
    ])),
    Matrix("Q", 0.5 * np.array([
        [-1, -rt(3)],
        [rt(3), -1]
    ])),
    Matrix("R", 0.5 * np.array([
        [-1, rt(3)],
        [-rt(3), -1]
    ])),
    Matrix("S", np.array([
        [1, 0],
        [0, -1]
    ])),
    Matrix("T", 0.5 * np.array([
        [-1, rt(3)],
        [rt(3), 1]
    ])),
    Matrix("U", 0.5 * np.array([
        [-1, -rt(3)],
        [-rt(3), 1]
    ]))
]

table = formCayleyTable(elements, operation, 0.0001)

mygroup4 = Group.fromCayleyTable(elements, table)

print("\n\nGroup 4")
print(mygroup4)