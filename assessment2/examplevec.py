""" Pre generated sets """
from util.vec import sp, generate_set

DIM = 4


def INDEP_SET():
    return generate_set(DIM, drop=[2])


def DEP_SET():
    return generate_set(DIM, dup=[2])


def WACK_SET():
    return generate_set(DIM, drop=[1], dup=[2])


def WIERDER_SET():
    return [
        sp.Matrix([2, 3, 0, 0]),
        sp.Matrix([5, -9, 1, 0])
    ]
