from constraint_satisfaction_problem import ConstraintSatisfactionProblem


class CircuitBoardProblem(ConstraintSatisfactionProblem):
    def __init__(self, board, parts):
        """
        :param board: the dimension of the board (width, height
        :param parts: list of the dimensions of the rectangular parts to place on the board
        """
        domains = dict()
        for i in range(board[0]):
            for j in range(board[1]):
                # for every part find the locations on the board that it can be placed and use that at it's domain
                for part in parts:
                    domains[part] = domains.get(part, set())
                    if i + part[0] <= board[0] and j + part[1] <= board[1]:
                        domains[part].add((i, j, part[0], part[1]))
        super().__init__(parts, domains)
        self.board = board

    @staticmethod
    def intersect(p1, p2):
        """
        :param p1: a rectangular part position assignment
        :param p2: a rectangular part position assignment
        :return: if the parts intersect
        """
        comp_parts = [p1, p2]
        comp_parts.sort(key=lambda x: x[0])
        x_lap = comp_parts[0][0] + comp_parts[0][2] > comp_parts[1][0]
        comp_parts.sort(key=lambda x: x[1])
        y_lap = comp_parts[0][1] + comp_parts[0][3] > comp_parts[1][1]
        return x_lap and y_lap

    def check_constraint(self, args):
        """
        :param args: check any assignment in the solution violated the constraint
        :return: if the solution assignments do not violate the constraint
        """
        for p in args:
            if args[p] is None:
                continue
            for other in self.variables:
                if args[other] is None:
                    continue
                if p != other and self.intersect(args[p], args[other]):
                    return False
        return True

    def write_board(self, solution):
        """
        :param solution: the solution
        :return: None
        print out the board with the rectangular parts represented on it
        """
        board = [['.' for x in range(self.board[0])] for y in range(self.board[1])]
        print(f"Board Dimensions: {self.board}")
        lt = 0
        for pos in solution.values():
            for i in range(pos[0], pos[0]+pos[2]):
                for j in range(pos[1], pos[1]+pos[3]):
                    board[j][i] = chr(lt+97)
            lt += 1
        print('\n'.join([''.join(x) for x in board]), '\n')

    def degree_heuristic(self, args):
        """
        :param args: args[0] is the variable, args[1] is the current csp solution
        this is using the idea that the part with the largest constraining power is the part with the largest area
        multiply by -1 to order the list appropirately
        """
        return -1 * args[0][0] * args[0][1]

    def remaining_values(self, args):
        """
        :param args: args[0] is the variable, args[1] is the current csp solution assignment
        :return valid domain values based on the current solution assignments
        this give the remaining valid domain values for a variable
        this goes through all the domain values for a variable and comparing with current assignments,
        it eliminates values in the domain that violate the constraint
        """
        domain = {x for x in self.domain[args[0]]}
        res = set()
        for adj in self.variables:
            d = args[1].assignment[adj]
            if d is not None:
                for o in domain:
                    if not self.intersect(o, d):
                        res.add(o)
        return res

    def mrv_heuristic(self, args):
        """
        :param args: args[0] is the variable, args[1] is the current csp solution assignment
        :return: the number of valid values contained in the domain of the variable
        """
        return len(self.remaining_values(args))

    def lcv_heuristic(self, args):
        """
        :param args: args[0] is the variable, args[1] is the value, args[1] is the current csp solution
        :return: the number of other values constrained by assigning this value
        tracks all other values constrained by assigning the value in args[1] to variable in args[0]
        """
        res = set()
        for adj in self.variables:
            if adj == args[0]:  # do not count the same variable
                continue
            domain = self.remaining_values((adj, args[2]))
            for o in domain:
                if self.intersect(args[1], o):
                    res.add(o)
        return len(res)


if __name__ == '__main__':
    _ = CircuitBoardProblem((10, 3), [(3, 2), (5, 2), (2, 3), (7, 1)])
    """"
    
        aaa  bbbbb  cc  ddddddd
        aaa  bbbbb  cc
                    cc
        0 1 2 3 4 5 6 7 8 9
      2 . . . . . . . . . .
      1 . . . . . . . . . .
      0 . . . . . . . . . .
    """
    _ = CircuitBoardProblem((7, 5), [(4, 3), (3, 4), (2, 2), (1, 2), (1, 2), (3, 1)])
    """"

        aaaa  bbb cc d eee
        aaaa  bbb cc d 
        aaaa  bbb
              bbb
              
        0 1 2 3 4 5 6
      4 . . . . . . .
      3 . . . . . . .
      2 . . . . . . .
      1 . . . . . . .
      0 . . . . . . .
    """


