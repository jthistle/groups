from texttable import Texttable
import math
from itertools import combinations

class Group:
    def __init__(self, elements):
        self.elements = elements
        self.order = len(elements)
        self.operation = None

    @classmethod
    def fromOperation(cls, elements, operation):
        grp = cls(elements)
        grp.operation = operation
        grp.generateCayleyTable()
        grp.cacheAttrs()
        return grp

    @classmethod
    def fromCayleyTable(cls, elements, table):
        grp = cls(elements)
        grp.cayleyTable = table
        grp.cacheAttrs()
        return grp

    def cacheAttrs(self):
        self.ident = self.getIdent()
        self.closed = self.isClosed()
        self.inversable = self.isInversable()
        self.valid = self.isGroup()
        if self.valid:
            self.elementOrders = [self.getElementOrder(x) for x in self.elements]
            self.generators = self.getGenerators()
        else:
            self.elementOrders = None
            self.generators = None

    def generateCayleyTable(self):
        self.cayleyTable = []
        for a in self.elements:
            column = []
            for b in self.elements:
                column.append(self.operation(a, b))
            self.cayleyTable.append(column)

    def getIdent(self):
        # TODO fix
        for r in range(self.order):
            isSame = True
            for c in range(self.order):
                if self.cayleyTable[c][r] != self.elements[c]:
                    isSame = False
                    break
            if isSame:
               return self.elements[r] 
        return None

    def getElementOrder(self, element):
        init = self.elements.index(element)
        last = element
        order = 1
        while last != self.ident:
            last = self.cayleyTable[self.elements.index(last)][init]
            order += 1
            if last == element:
                print("Seems like this set doesn't form a group under the given operation ({} {})".format(element, order))
                break
        return order

    def getGenerators(self):
        gens = []
        for i in range(self.order):
            order = self.elementOrders[i]
            if order == self.order:
                gens.append(self.elements[i])
        return gens

    def isCyclic(self):
        return len(self.generators) != 0

    def isClosed(self):
        closed = True
        for c in self.cayleyTable:
            for el in c:
                if el not in self.elements:
                    closed = False
                    break
        return closed

    def isInversable(self):
        inverse = True
        for c in self.cayleyTable:
            hasInverse = False
            for el in c:
                if el == self.ident:
                    hasInverse = True
                    break
            if not hasInverse:
                inverse = False
                break
        return inverse

    def isGroup(self):
        return self.ident is not None and self.closed and self.inversable

    def inverse(self, element):
        c = self.cayleyTable[self.elements.index(element)]
        for i in range(len(c)):
            if c[i] == self.ident:
                return self.elements[i]
        return None

    # Non-trivial and proper only
    def subgroups(self):
        subgroups = []
        for i in range(1, math.ceil(self.order / 2) + 1):
            if self.order % i != 0:
                # Laplace theorem
                continue
            for combo in combinations(self.elements, i):
                if i == 1 and combo[0] == self.ident:
                    continue

                byInd = [self.elements.index(x) for x in combo]
                newCayley = []
                for c in byInd:
                    column = []
                    for r in byInd:
                        column.append(self.cayleyTable[c][r])
                    newCayley.append(column)

                newGrp = Group.fromCayleyTable(combo, newCayley)
                if self.operation is not None:
                    newGrp.operation = self.operation
                if newGrp.isGroup():
                    subgroups.append(newGrp)
        return subgroups

    def strCayleyTable(self):
        cayley = Texttable()

        rows = []
        rows.append(["."] + list(self.elements))
        for r in range(self.order):
            row = [self.elements[r]]
            for c in range(self.order):
                row.append(self.cayleyTable[c][r])
            rows.append(row)

        cayley.add_rows(rows)

        return cayley.draw()
        
    def validStr(self):
        orderTable = Texttable()
        rows = []
        rows.append(["Element:"] + self.elements)
        rows.append(["Order:"] + self.elementOrders)
        rows.append(["Inverse:"] + [self.inverse(x) for x in self.elements])
        orderTable.add_rows(rows)

        gens = ", ".join([str(x) for x in self.generators]) or "None"

        sub = self.subgroups()
        subGrpStr = "\n".join([str([str(y) for y in x.elements]) for x in sub])

        return """
Is a group: {}
Group order {}, identity {}
Cayley table: \n{}

Orders: \n{}

Generators: {}

Cyclic: {}

Non-trivial & proper subgroups: \n{}
""".format(self.isGroup(), self.order, self.ident, self.strCayleyTable(), orderTable.draw(), gens, self.isCyclic(), subGrpStr)

    def invalidStr(self):
        return """
Not a group! One of these failed:
Inversable: {}
Closed: {}
Identity: {}

Cayley table: \n{}
""".format(self.inversable, self.closed, self.ident, self.strCayleyTable())

    def __str__(self):
        if self.valid:
            return self.validStr()
        else:
            return self.invalidStr()

def visibleToInternal(table):
    """Convert a visible table in form [row][column] to internal format of [column][row]"""
    new = []
    for i in range(len(table)):
        c = []
        for j in range(len(table[i])):
            c.append(table[j][i])
        new.append(c)
    return new


class Element:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def isApproxEq(self, b, approximation):
        return abs(b.value - self.value) <= approximation

    def __str__(self):
        return self.name

import numpy

def formCayleyTable(elements, operation, approximation):
    table = []
    for a in elements:
        c = []
        for b in elements:
            value = operation(a, b)
            found = False
            for e in elements:
                if e.isApproxEq(value, approximation):
                    c.append(e)
                    found = True
                    break
            if not found:
                print("Couldn't find same element in set!")
                return False
        table.append(c)
    return table