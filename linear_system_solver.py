import copy


def solve_system_two_unknowns(a_1, b_1, c_1, a_2, b_2, c_2):
    """Implementation of the Algorithm 1"""
    if a_2 * b_1 - a_1 * b_2 == 0:
        if a_1 * c_2 == c_1 * a_2:  # Same as a_1 / a_2 == c_1 / c_2
            return "Infinitely many solutions"
        else:
            return "No solutions"

    else:
        x = (b_1 * c_2 - b_2 * c_1) / (a_2 * b_1 - a_1 * b_2)
        y = (a_1 * c_2 - a_2 * c_1) / (b_2 * a_1 - b_1 * a_2)
        return x, y


def reduce_system(system: list[list[int]]):
    """Implementation of the Algorithm 2"""
    n = len(system)
    result = copy.deepcopy(system)
    for i in range(1, n):  # we work with zero-based indexing
        for j in range(0, n - 1):  # same
            result[i][j] += (-system[0][j] / system[0][n - 1]) * system[i][n - 1]
        result[i][-1] -= (system[0][-1] / system[0][n - 1]) * system[i][n - 1]
        del result[i][n - 1]
    del result[0]
    return result


def ensure_non_zero_coefs(system: list[list[int]]):
    """Implementation of the Algorithm 4"""
    result = copy.deepcopy(system)
    n = len(system)
    i = 0
    while i != n:
        j = 0
        while j != n:
            if result[i][j] == 0:
                for m in range(0, n):  # picking m
                    if result[m][j] != 0:
                        break

                for k in range(0, n):
                    result[i][k] += result[m][k]
                result[i][-1] += result[m][-1]

                j = 0

            else:
                j += 1
        i += 1
    return result


def solve_system(system: list[list[int]]) -> tuple[int]:
    """Implementation of the Algorithm 5"""
    system = ensure_non_zero_coefs(system)
    n = len(system)
    if n == 2:
        return solve_system_two_unknowns(*system[0], *system[1])
    else:
        reduced_system = reduce_system(system)
        solutions_found = solve_system(reduced_system)
        if not isinstance(solutions_found, tuple):
            # Infinitely many or no solutions
            return solutions_found

        reduced_system = ensure_non_zero_coefs(reduced_system)

        x_n = 0
        for m in range(0, n - 1):
            x_n -= (system[0][m] / system[0][n - 1]) * solutions_found[m]

        x_n += system[0][-1] / system[0][n - 1]

        return solutions_found + (x_n,)
