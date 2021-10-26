from constraint_satisfaction_problem import ConstraintSatisfactionProblem


class CircuitBoardProblem(ConstraintSatisfactionProblem):

    def __init__(self, board, parts):
        domains = dict()
        for i in range(board[0]):
            for j in range(board[1]):
                for part in parts:
                    domains[part] = domains.get(part, set())
                    if i + part[0] <= board[0] and j + part[1] <= board[1]:
                        domains[part].add((i, j, part[0], part[1]))
                    # if i + part[1] <= board[0] and j + part[0] <= board[1]:
                    #     domains[part].add((i, j, part[1], part[0]))
        super().__init__(parts, domains)
        self.indices = {self.variables[i]: i for i in range(len(self.variables))}
        self.board = board

    @staticmethod
    def intersect(p1, p2):
        comp_parts = [p1,p2]
        comp_parts.sort(key=lambda x: x[0])
        x_lap = comp_parts[0][0] + comp_parts[0][2] > comp_parts[1][0]
        comp_parts.sort(key=lambda x: x[1])
        y_lap = comp_parts[0][1] + comp_parts[0][3] > comp_parts[1][1]
        return x_lap and y_lap

    def check_constraint(self, args):
        for i in range(len(args)):
            if args[i] is None:
                continue
            for other in self.variables:
                j = self.indices[other]
                if args[j] is None:
                    continue
                if i != j and self.intersect(args[i], args[j]):
                    return False
        return True

    def mapping_to_solution(self, args):
        return {p: args[self.indices[p]] for p in self.variables}

    def write_board(self, solution):
        board = [['.' for x in range(self.board[0])] for y in range(self.board[1])]
        print(f"Board Dimensions: {self.board}")
        lt = 0
        for pos in solution:
            # print(pos,  chr(lt+97))
            for i in range(pos[0], pos[0]+pos[2]):
                for j in range(pos[1], pos[1]+pos[3]):
                    board[j][i] = chr(lt+97)
            lt += 1
        print('\n'.join([''.join(x) for x in board]), '\n')

    def degree_heuristic(self, args):
        """
        :param args: args[0] is the variable
        :return:
        """
        return -1 * args[0][0] * args[0][1]

    def remaining_values(self, args):
        """
        :param args: args[0] is the variable, args[1] is the current csp solution
        :return:
        """
        domain = {x for x in self.domain[args[0]]}
        res = set()
        for adj in self.variables:
            d = args[1].assignment[self.indices[adj]]
            if d is not None:
                for o in domain:
                    if not self.intersect(o, d):
                        res.add(o)
        return res

    def mrv_heuristic(self, args):
        return len(self.remaining_values(args))

    def lcv_heuristic(self, args):
        """
        :param args: args[0] is the variable, args[1] is the value, args[1] is the current csp solutiopn
        :return:
        """
        count = 0
        for adj in self.variables:
            if adj == args[0]:
                continue
            domain = self.remaining_values((adj, args[2]))
            res = set()
            for o in domain:
                if self.intersect(args[1], o):
                    res.add(o)
            count += len(res)
        return count

    def apply_sort_to_indices(self):
        self.indices = {self.variables[i]: i for i in range(len(self.variables))}


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


