from constraint_satisfaction_problem import ConstraintSatisfactionProblem


class ColorMappingProblem(ConstraintSatisfactionProblem):

    def __init__(self, adjacent_countries):
        self.red = (1, 0, 0)
        self.blue = (0, 0, 1)
        self.green = (0, 1, 0)
        super().__init__([x for x in adjacent_countries],
                         {x: [self.red, self.blue, self.green] for x in adjacent_countries})
        self.indices = {self.variables[i]: i for i in range(len(self.variables))}
        self.adjacent_countries = adjacent_countries

    def check_constraint(self, args):
        for i in range(len(args)):
            if args[i] is None:
                continue
            country = self.variables[i]
            for adj in self.adjacent_countries[country]:
                adj_index = self.indices[adj]
                if args[adj_index] == args[i]:
                    return False
        return True

    def mapping_to_solution(self, args):
        return {c: args[self.indices[c]] for c in self.variables}

    def degree_heuristic(self, args):
        return len(self.adjacent_countries[args[0]])

    def remaining_values(self, args):
        domain = {x for x in self.domain[args[0]]}
        for adj in self.adjacent_countries[args[0]]:
            d = args[1].assignment[self.indices[adj]]
            if d is not None and d in domain:
                domain.remove(d)
        return domain

    def mrv_heuristic(self, args):
        return len(self.remaining_values(args))

    def lcv_heuristic(self, args):
        count = 0
        for adj in self.adjacent_countries[args[0]]:
            domain = self.remaining_values((adj, args[2]))
            if args[1] in domain:
                domain.remove(args[1])
            count += len(domain)
        return -count

    def apply_sort_to_indices(self):
        self.indices = {self.variables[i]: i for i in range(len(self.variables))}
