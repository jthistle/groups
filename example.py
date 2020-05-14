#!/usr/bin/env python3

from libgroups import Group, visibleToInternal
from libpermutations import generateGroup

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

print(mygroup3)