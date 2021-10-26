import cProfile
from constrain_satisfactions_solution import Solution
from circuit_board_problem import CircuitBoardProblem
from constrain_satisfaction import backtracking_search


USE_LOGGER = False  # set this value to true to see cProfile performance log
USE_DEGREE_HEURISTIC = False  # toggle this value to apply the Degree Heuristic
USE_MRV_HEURISTIC = True  # toggle this value to apply the MRV Heuristic
USE_LCV_HEURISTIC = False  # toggle this value to apply the LCV Heuristic

p1 = CircuitBoardProblem((10, 3), [(3, 2), (5, 2), (2, 3), (7, 1)])
s1 = Solution("Back Track Search Solution")
if USE_LOGGER:
    cProfile.run('backtracking_search(s1, p1, degree_heuristic=True)')
else:
    backtracking_search(s1, p1, degree_heuristic=USE_DEGREE_HEURISTIC, mrv_heuristic=USE_MRV_HEURISTIC,
                        lcv_heuristic=USE_LCV_HEURISTIC)
print(s1)
if s1.isComplete:  # only show solution if there is a solution
    p1.write_board(s1.assignment)


p2 = CircuitBoardProblem((7, 5), [(4, 3), (3, 4), (1, 2), (2, 2), (3, 1)])
s2 = Solution("Back Track Search Solution")
if USE_LOGGER:
    cProfile.run('backtracking_search(s2, p2, degree_heuristic=True)')
else:
    backtracking_search(s2, p2, degree_heuristic=USE_DEGREE_HEURISTIC, mrv_heuristic=USE_MRV_HEURISTIC,
                        lcv_heuristic=USE_LCV_HEURISTIC)
print(s2)
if s2.isComplete:  # only show solution if there is a solution
    p2.write_board(s2.assignment)
