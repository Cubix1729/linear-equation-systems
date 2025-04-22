from linear_system_solver import solve_system
from fractions import Fraction
from random import randint, choice
from sympy import Matrix, EmptySet
from sympy.solvers.solveset import linsolve
import copy


def system_to_fractions(system) -> list[list[Fraction]]:
    result = copy.deepcopy(system)
    for i in range(len(result)):
        for j in range(len(result) + 1):
            result[i][j] = Fraction(result[i][j])

    return result


def random_system(size):
    return [[randint(-15, 15) for _ in range(size + 1)] for _ in range(size - 1)] + [
        [choice([randint(-15, -1), randint(1, 15)]) for _ in range(size + 1)]
    ]


def test_random_systems(max_size=10, num_systems=1000):
    for _ in range(num_systems):
        system = random_system(randint(2, max_size))
        print("Testing:", system)
        found_solutions = solve_system(system_to_fractions(system))
        sympy_solutions = linsolve(Matrix(system))

        if found_solutions == "Infinitely many solutions":
            continue

        elif found_solutions == "No solutions":
            assert (
                sympy_solutions == EmptySet
            ), f"no solutions were found for system {system}, but solutions do exist"
            continue

        for solution_index in range(len(found_solutions)):
            found_solution = found_solutions[solution_index]
            sympy_solution = list(sympy_solutions)[0][solution_index]

            assert (
                found_solution == sympy_solution
            ), f"invalid solution (found: {found_solution}, expected: {sympy_solution}) for system {system}"

    print(f"All tests passed (with {num_systems} systems of up to {max_size} equations)")


if __name__ == "__main__":
    test_random_systems()
