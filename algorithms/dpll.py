import sys, os
from itertools import chain

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from syntax import *
from cnf import to_cnf


class DPLL:
    def __init__(self, kb: Conjunction, query: Symbol):
        self.kb = kb
        self.query = query
        self.clauses = self.initialize_clauses()

    def initialize_clauses(self):
        kb_cnf = to_cnf(self.kb)
        query_negated = to_cnf(self.query.negate())
        combined_clauses = Conjunction(kb_cnf, query_negated)
        return {clause for clause in combined_clauses.args}

    def solve(self):
        # print("Clauses:", self.clauses)
        valid = self.dpll(self.clauses)
        if valid:
            print('YES')
        else:
            print('NO')

    def dpll(self, clauses:set[Sentence]):
        # Unit propagation
        unit_clauses = {clause for clause in clauses if self.is_literal(clause)}
        while unit_clauses:
            # print("Unit Clauses:", unit_clauses)
            for unit_clause in unit_clauses:
                clauses = self.unit_propagate(unit_clause, clauses)
            # print("Clauses after UP:", clauses)
            unit_clauses = {clause for clause in clauses if self.is_literal(clause)}
            
        # Pure literal elimination
        pure_literals = self.find_pure_literals(clauses)
        # print("Pure Literals:", pure_literals)
        for literal in pure_literals:
            clauses = self.pure_literal_assign(literal, clauses)
        # print("Clauses after PLE:", clauses)
        
        # Stopping conditions
        if not clauses:
            return False
        if any(clause == 0 for clause in clauses):
            # Clauses contain an empty clause, which means the KB ^ ~Q is unsatisfiable
            return True
        
        # DPLL recursion
        literal = next(iter(clauses)).symbols().pop()
        # print("Literal:", literal)
        return self.dpll(clauses.union({literal})) or self.dpll(clauses.union({literal.negate()}))
        
    def is_literal(self, clause:Sentence) -> bool:
        if isinstance(clause, Symbol):
            return True
        return isinstance(clause, Negation) and isinstance(clause.arg, Symbol)
    
    def contains_literal(self, literal:Symbol|Negation, clause:Sentence) -> bool:
        if literal == clause:
            return True
        if isinstance(clause, CommutativeSentence):
            return any(literal == arg for arg in clause.args)
        return False
    
    def unit_propagate(self, literal:Symbol|Negation, clauses:set[Sentence]) -> set[Sentence]:
        new_clauses = set()
        for clause in clauses:
            if self.contains_literal(literal, clause):
                continue
            if self.contains_literal(literal.negate(), clause):
                if isinstance(clause, Disjunction):
                    args = [arg for arg in clause.args if arg != literal.negate()]
                    # print("ARGS", args)
                    if len(args) > 1:
                        new_clause = Disjunction(*args)
                    else:
                        new_clause = args[0]
                    new_clauses.add(new_clause)
                elif clause == literal.negate():
                    new_clauses.add(0)
                else:
                    print("UP", literal, clause, clauses)
            else:
                new_clauses.add(clause)
        return new_clauses
    
    def is_pure_literal(self, literal:Symbol|Negation, clauses:set[Sentence]) -> bool:
        positive = any(self.contains_literal(literal, clause) for clause in clauses)
        negative = any(self.contains_literal(literal.negate(), clause) for clause in clauses)
        return positive != negative
    
    def find_pure_literals(self, clauses:set[Sentence]) -> set[Symbol|Negation]:
        pure_literals = set()
        for clause in clauses:
            if clause == 0:
                continue
            for symbol in clause.symbols():
                if self.is_pure_literal(symbol, clauses):
                    pure_literals.add(symbol)
        return pure_literals
    
    def pure_literal_assign(self, literal:Symbol|Negation, clauses:set[Sentence]) -> set[Sentence]:
        return set([clause for clause in clauses if not self.contains_literal(literal, clause)])


if __name__ == "__main__":
    from parser import parse_kb_and_query
    file_name = 'test_dpll.txt'
    kb, query = parse_kb_and_query(file_name)
    print(f"Knowledge Base: {kb}")
    print(f"Query: {query}")

    dpll = DPLL(kb, query)
    dpll.solve()
