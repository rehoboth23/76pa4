import cProfile
from constrain_satisfactions_solution import Solution
from map_coloring_problem import MapColoringProblem
from constrain_satisfaction import backtracking_search


USE_LOGGER = False  # set this value to true to see cProfile performance log
USE_DEGREE_HEURISTIC = False  # toggle this value to apply the Degree Heuristic
USE_MRV_HEURISTIC = True  # toggle this value to apply the MRV Heuristic
USE_LCV_HEURISTIC = False  # toggle this value to apply the LCV Heuristic

countries = {
    'WA': ['NT', 'SA'],
    'NT': ['Q', 'SA', 'WA'],
    'Q': ['NT', 'NSW', 'SA'],
    'NSW': ['Q', 'SA', 'V'],
    'V': ['NSW', 'SA'],
    'SA': ['NT', 'NSW', 'Q', 'V', 'WA'],
    'T': []
}
p1 = MapColoringProblem(countries)
s1 = Solution("back track search solution")
if USE_LOGGER:
    cProfile.run('backtracking_search(s1, p1, degree_heuristic=USE_DEGREE_HEURISTIC, mrv_heuristic=USE_MRV_HEURISTIC)')
else:
    backtracking_search(s1, p1, degree_heuristic=USE_DEGREE_HEURISTIC, mrv_heuristic=USE_MRV_HEURISTIC,
                        lcv_heuristic=USE_LCV_HEURISTIC)
print(s1)
