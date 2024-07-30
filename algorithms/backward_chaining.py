import sys, os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from syntax import *
from parser import parse_kb_and_query


class BackwardChaining:
    def __init__(self, kb: Conjunction, query: Symbol):
        self.kb = kb
        self.query = query
        self.check_kb()
        self.check_query()

    def solve(self):
        solution_found, chain = self.prove(self.query, [], set())
        if solution_found:
            print(f"YES: {', '.join([symbol.name for symbol in chain])}")
        else:
            print("NO")
        
    def check_kb(self):
        if isinstance(self.kb, (Implication, Symbol)):
            return True
        for clause in self.kb.args:
            if not isinstance(clause, (Implication, Symbol)):
                print("Warning: Knowledge base is not in Horn form. The algorithm may not function correctly.")
                return False
        return True

    def check_query(self):
        if not isinstance(self.query, Symbol):
            print("Warning: Query is not a symbol. The algorithm may not function correctly.")
            return False
        return True

    def prove(self, goal:Symbol, chain:list[Symbol], visited:set[Symbol]):
        # print(goal, chain, visited)
        if goal in visited:
            return False, chain
        visited.add(goal)
        
        clauses = self.kb.args if isinstance(self.kb, Conjunction) else [self.kb]
        # Check if the goal is a fact in the KB
        for clause in clauses:
            if isinstance(clause, Symbol) and clause == goal:
                chain.append(goal)
                return True, chain
            # Check if the goal can be derived from implications in the KB
            if isinstance(clause, Implication) and clause.consequent == goal:
                all_true = True
                for subgoal in clause.antecedent.symbols():
                    established, chain = self.prove(subgoal, chain, visited)
                    if not established:
                        all_true = False
                        break
                if all_true:
                    chain.append(goal)
                    return True, chain

        return False, chain

    
if __name__ == "__main__":
    # file_name = 'test_genericKB.txt'
    file_name = 'test_HornKB.txt'
    kb, query = parse_kb_and_query(file_name)
    print(f"Knowledge Base: {kb}")
    print(f"Query: {query}")
    
    bc = BackwardChaining(kb, query)
    bc.solve()

