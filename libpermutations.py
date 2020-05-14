

from libgroups import Group

def areSamePerm(a, b):
    for i in range(len(a)):
        if a[i] != b[i]:
            return False
    return True


def generateGroup(elements, permutations):
    cayleyTable = []

    for i in range(len(elements)):
        firstPerm = permutations[i]
        c = []
        for j in range(len(elements)):
            secondPerm = permutations[j]
            final = [firstPerm[x] for x in secondPerm]
            success = False
            for k in range(len(elements)):
                if areSamePerm(final, permutations[k]):
                    c.append(elements[k])
                    success = True
                    break
            if not success:
                print("Uh oh! Permutation of {} * {} = {} is not another permutation in group!".format(elements[i], elements[j], final))
                return None

        cayleyTable.append(c)

    return Group.fromCayleyTable(elements, cayleyTable)
    