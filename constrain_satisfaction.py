from constrain_satisfactions_solution import Solution
from constraint_satisfaction_problem import ConstraintSatisfactionProblem


def degree_heuristic_sort(problem: ConstraintSatisfactionProblem, solution: Solution):
    problem.variables.sort(key=lambda x: problem.degree_heuristic((x, solution)))
    problem.apply_sort_to_indices()


def mrv_heuristic_sort(problem: ConstraintSatisfactionProblem, solution: Solution):
    problem.variables.sort(key=lambda x: problem.mrv_heuristic((x, solution)))
    problem.apply_sort_to_indices()


def lcv_heuristic_sort(problem: ConstraintSatisfactionProblem, variable, solution: Solution):
    problem.domain[variable] = sorted(problem.domain[variable],
                                      key=lambda x: problem.lcv_heuristic((variable, x, solution)))
    problem.apply_sort_to_indices()


def backtracking_search(solution: Solution, problem: ConstraintSatisfactionProblem,
                        degree_heuristic=False, mrv_heuristic=False, lcv_heuristic=False):
    """
    :param solution: solution object for the csp problem. the actual solution is in solution.assignment
    :param problem: the csp problem to solve
    :return: if problem is solved. problem is solved if the current assignment satisfies the constrain and the number of
    assignments is equal to the number of variable in the problem
    :param lcv_heuristic:
    :param mrv_heuristic:
    :param degree_heuristic:
    """
    if not len(solution.assignment):
        solution.assignment = [None for _ in problem.variables]
    if mrv_heuristic:
        mrv_heuristic_sort(problem, solution)
    if degree_heuristic:
        degree_heuristic_sort(problem, solution)
    for i in range(len(problem.variables)):
        v = problem.variables[i]
        if solution.assignment[i] is not None:  # do not reassign a problem if it has already been assigned
            continue
        if lcv_heuristic:
            lcv_heuristic_sort(problem, v, solution)
        for d in problem.domain[v]:  # try every possible assignment in a variables domain
            solution.nodes_visited += 1  # count variable assignments made
            solution.assignment[i] = d  # assign value to variable
            if problem.check_constraint(solution.assignment):  # check if the current assignment violated the constrain
                backtracking_search(solution, problem, degree_heuristic=degree_heuristic,
                                    mrv_heuristic=mrv_heuristic, lcv_heuristic=lcv_heuristic)
                if solution.isComplete:  # check if the solution is complete on return
                    return
            # if the solution is not complete or the assignment violated the constraint rules remove the assignment
            solution.assignment[i] = None
        if v not in solution.assignment:
            return
    solution.isComplete = problem.check_constraint(solution.assignment) and \
                          len(solution.assignment) == len(problem.variables)

