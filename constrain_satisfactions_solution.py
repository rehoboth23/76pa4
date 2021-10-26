
class Solution:
    def __init__(self, name):
        self.name = name
        self.isComplete = False
        self.assignment = []
        self.nodes_visited = 0

    def __str__(self):
        return f"Name: {self.name}\nIs Complete: {self.isComplete}\nSolution: {self.assignment}" \
               f"\nNodes Visited: {self.nodes_visited}"
