from constraint_satisfaction_problem import ConstraintSatisfactionProblem


class MapColoringProblem(ConstraintSatisfactionProblem):

    def __init__(self, adjacent_countries):
        self.red = (1, 0, 0)
        self.blue = (0, 0, 1)
        self.green = (0, 1, 0)
        super().__init__([x for x in adjacent_countries],
                         {x: [self.red, self.blue, self.green] for x in adjacent_countries})
        self.adjacent_countries = adjacent_countries

    def check_constraint(self, args):
        """
        :param args: args is the current csp solution assignment
        :return: if no variable: value assignment in the solution violates the constraint
        """
        for c in args:
            if args[c] is None:
                continue
            for adj in self.adjacent_countries[c]:
                if args[c] == args[adj]:
                    return False
        return True

    def degree_heuristic(self, args):
        """
        :param args: args[0] is the variable, args[1] is the current csp solution
        :return: the number of other locations adjacent to the current location who are not yet assigned values
        in the solution
        """
        return len([x for x in self.adjacent_countries[args[0]] if args[1].assignment[x] is not None])

    def remaining_values(self, args):
        """
           :param args: args[0] is the variable, args[1] is the current csp solution assignment
           :return valid domain values based on the current solution assignments
           this give the remaining valid domain values for a variable
           this goes through all the domain values for a variable and comparing with current assignments,
           it eliminates values in the domain that violate the constraint
        """
        domain = {x for x in self.domain[args[0]]}
        for adj in self.adjacent_countries[args[0]]:
            d = args[1].assignment[adj]
            if d is None and d in domain:
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
