from util.vec import process_set, sp

"""
BEHAVIOR:

Not spanning:
- RREF has at least one all zero row
therefore -> make it dependent, and cut it back down

Dependent:
- RREF has no all zero rows
- RREF has at least one row with more than a single one
- Pivot columns exclude extra columns
therefore -> find non-pivot and remove
finally, it yields a basis

"""


def basis(op_set):
    while True:
        rref, pivot = process_set(op_set)  # process
        set_dim = rref.rows

        print("Set:", op_set)

        print("\nRREF:", rref)

        print("\nPivot:", pivot)

        # Check if set is spanning
        spanning = True
        for i_r in range(set_dim):
            if 1 not in rref.row(i_r):
                spanning = False
                break

        if not spanning:
            # Add all basic basis vectors until to ensure is dependent:
            for i_element in range(set_dim):
                new_v = [0]*set_dim
                new_v[i_element] = 1
                op_set.append(sp.Matrix(new_v))
            # is NOW SPANNING and DEPENDENT
        else:
            # Need to check for dependency and remove necessary rows to make it independent

            # Get columns not in pivot set:
            dep_cols = set(range(len(op_set))).difference(pivot)

            # Remove these dependent columns from set
            #   (run in reverse order to prevent indexing misalignment)
            for rem_col in sorted(dep_cols, reverse=True):
                del op_set[rem_col]

            return op_set
