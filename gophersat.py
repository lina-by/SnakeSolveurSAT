# TODO: functions that translate the list of constaints into a cnf file and interpret the gophersat output
import os
from itertools import combinations, product
from typing import Tuple, Callable


def create_variable_index(N: int, T: int, nb_pommes: int = 0) -> Callable:
    index_position = {
        (x, y, t): N**2 * t + N * y + x + 1
        for x, y, t in product(range(N), range(N), range(T))
    }
    index_pommes = {
        (p, t): N**2 * T + p * T + t + 1 for p in range(nb_pommes) for t in range(T)
    }
    index_counter = {
        (c, t): N**2 * T + nb_pommes * T + c * T + t + 1
        for c in range(nb_pommes)
        for t in range(T)
    }

    def variable(id, typ: str = "s"):
        if typ == "s":
            if not (
                isinstance(id, tuple)
                and len(id) == 3
                and all(isinstance(i, int) for i in id)
            ):
                raise TypeError(
                    "Wrong id format for snake position. Expected a tuple (int, int, int)."
                )
            x, y, t = id
            if x >= N:
                raise ValueError("x is above N")
            if y >= N:
                raise ValueError("y is above N")
            if t >= T:
                raise ValueError("t is above T")
            return index_position[id]

        if typ == "p":
            if not isinstance(id, tuple) or len(id) != 2:
                raise TypeError(
                    "Wrong id format for apple. Expected an tuple of len 2 ."
                )
            if id[0] >= nb_pommes:
                raise ValueError("Apple index is over the limit")
            if id[1] >= T:
                raise ValueError("Time index is over the limit")
            return index_pommes[(id[0], id[1])]

        if typ == "c":
            if not isinstance(id, tuple) or len(id) != 2:
                raise TypeError(
                    "Wrong id format for counter. Expected an tuple of len 2 ."
                )
            if id[0] >= nb_pommes:
                raise ValueError("Counter index is over the limit")
            if id[1] >= T:
                raise ValueError("Time index is over the limit")
            return index_counter[(id[0], id[1])]

        raise ValueError(
            "Invalid type. 'typ' must be 's' for snake, 'p' for apple or 'c' for counter."
        )

    return variable


def format_clause(litteraux: list[int]):
    clause = ""
    for lit in litteraux:
        clause += f"{lit} "
    clause += "0\n"
    return clause


def create_sat(N_variables, clauses):
    with open("./table.cnf", "w") as f:
        f.write(f"p cnf {N_variables} {len(clauses)}\n")

        for clause in clauses:
            f.write(clause)

    result = os.popen("gophersat table.cnf").read()
    if result.split()[-1] == "UNSATISFIABLE":
        return []

    result = result.split()
    return [int(x) for x in result[-N_variables - 1 : -1]]
