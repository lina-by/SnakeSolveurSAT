# TODO: functions that translate the list of constaints into a cnf file and interpret the gophersat output
import os


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
