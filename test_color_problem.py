import cProfile
import sys

from constrain_satisfactions_solution import Solution
from color_problem import ColorMappingProblem
from constrain_satisfaction import backtracking_search


USE_LOGGER = False  # set this value to true to see cProfile performance log
USE_DEGREE_HEURISTIC = False
USE_MRV_HEURISTIC = True
USE_LCV_HEURISTIC = False

countries = {
    'WA': ['NT', 'SA'],
    'NT': ['Q', 'SA', 'WA'],
    'Q': ['NT', 'NSW', 'SA'],
    'NSW': ['Q', 'SA', 'V'],
    'V': ['NSW', 'SA'],
    'SA': ['NT', 'NSW', 'Q', 'V', 'WA'],
    'T': []
}
p1 = ColorMappingProblem(countries)
s1 = Solution("back track search solution")
if USE_LOGGER:
    cProfile.run('backtracking_search(s1, p1, degree_heuristic=USE_DEGREE_HEURISTIC, mrv_heuristic=USE_MRV_HEURISTIC)')
else:
    backtracking_search(s1, p1, degree_heuristic=USE_DEGREE_HEURISTIC, mrv_heuristic=USE_MRV_HEURISTIC,
                        lcv_heuristic=USE_LCV_HEURISTIC)
print(s1)
print(p1.mapping_to_solution(s1.assignment))

