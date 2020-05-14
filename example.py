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