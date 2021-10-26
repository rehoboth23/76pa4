from constrain_satisfactions_solution import Solution
from constraint_satisfaction_problem import ConstraintSatisfactionProblem


def degree_heuristic_sort(problem: ConstraintSatisfactionProblem, solution: Solution):
    """
    :param problem: the csp problem
    :param solution: the csp solution at this point
    sorts the problem variables according to the dergree heuristic
    """
    problem.variables.sort(key=lambda x: problem.degree_heuristic((x, solution)))


def mrv_heuristic_sort(problem: ConstraintSatisfactionProblem, solution: Solution):
    """
    :param problem: the csp problem
    :param solution: the csp solution at this point
    sorts the problem variables according to the heuristic
    """
    problem.variables.sort(key=lambda x: problem.mrv_heuristic((x, solution)))


def lcv_heuristic_sort(problem: ConstraintSatisfactionProblem, variable, solution: Solution):
    """
    :param problem: the csp problem
    :param variable: the variable being considered
    :param solution: the csp solution at this point
    sorts the domain problem variable according to the lcv heuristic
    """
    problem.domain[variable] = sorted(problem.domain[variable],
                                      key=lambda x: problem.lcv_heuristic((variable, x, solution)))


def backtracking_search(solution: Solution, problem: ConstraintSatisfactionProblem,
                        degree_heuristic=False, mrv_heuristic=False, lcv_heuristic=False):
    """
    :param solution: solution object for the csp problem. the actual solution is in solution.assignment
    :param problem: the csp problem to solve
    :return: if problem is solved. problem is solved if the current assignment satisfies the constrain and the number of
    assignments is equal to the number of variable in the problem
    :param lcv_heuristic: toggle to use the lcv heuristic
    :param mrv_heuristic: toggle to use the mrv heuristic
    :param degree_heuristic: toggle to use the degree heuristic

    """
    if solution.assignment is None:
        solution.assignment = {v: None for v in problem.variables}
    if mrv_heuristic:
        mrv_heuristic_sort(problem, solution)
    if degree_heuristic:
        degree_heuristic_sort(problem, solution)
    for i in range(len(problem.variables)):
        v = problem.variables[i]
        if solution.assignment[v] is not None:  # do not reassign a problem if it has already been assigned
            continue
        if lcv_heuristic:
            lcv_heuristic_sort(problem, v, solution)
        for d in problem.domain[v]:  # try every possible assignment in a variables domain
            solution.nodes_visited += 1  # count variable assignments made
            solution.assignment[v] = d  # assign value to variable
            if problem.check_constraint(solution.assignment):  # check if the current assignment violated the constrain
                backtracking_search(solution, problem, degree_heuristic=degree_heuristic,
                                    mrv_heuristic=mrv_heuristic, lcv_heuristic=lcv_heuristic)
                if solution.isComplete:  # check if the solution is complete on return
                    return
            # if the solution is not complete or the assignment violated the constraint rules remove the assignment
            solution.assignment[v] = None
        if solution.assignment[v] is None:
            return
    solution.isComplete = problem.check_constraint(solution.assignment) and \
                          all(solution.assignment[x] is not None for x in solution.assignment)

