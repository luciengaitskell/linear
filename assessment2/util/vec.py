import sympy as sp


def process_set(set_list):
    """
    :param set_list: array[Matrix] - the vector set to process
    :return: Tuple[rref, set(pivots)]
    """
    s_equation = sp.BlockMatrix([set_list])  # Combine vectors horizontally
    s_rref = s_equation.as_explicit().rref()  # Get RREF information of vector equation

    return s_rref[0], set(s_rref[1])


def generate_set(dim, drop: list = None, dup: list = None):
    """
    Generate simple test set based on characteristics

    :param dim: Dimension of the vectors
    :param drop: Vector index to drop
    :param dup: Vector index to duplicate
    :return: list[sp.Matrix]
    """
    s = []
    for i in range(dim):
        if drop is not None and i in drop:
            continue

        if dup is not None and i in dup:
            count = 2
        else:
            count = 1

        for j in range(0, count):
            v = [0] * dim
            v[i] = 1
            s.append(sp.Matrix(v))
    return s
