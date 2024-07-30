import sys, os
import itertools

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from syntax import *
from parser import parse_kb_and_query
from cnf import to_cnf


class DPLL:
    def __init__(self, kb: Conjunction, query: Symbol):
        self.kb = kb
        self.query = query
        # self.symbols = sorted(kb.symbols() | query.symbols(), key=lambda x: x.name)
        # self.symbols_map = {symbol.name: symbol for symbol in self.symbols}
        # self.model = {}
        # self.valid = False
        self.clauses = self.initialize_clauses()
        
    def initialize_clauses(self):
        kb_cnf = to_cnf(self.kb)
        query_negated = to_cnf(Negation(self.query))
        combined_clauses = Conjunction(kb_cnf, query_negated)
        return set([clause for clause in combined_clauses.args])
    
    def solve(self):
        model = {}
        valid = self.dpll(self.clauses, model)
        if valid:
            print('YES')
        else:
            print('NO')
            
    def dpll(self, clauses:set[Sentence], assignment):
        clauses, assignment = self.unit_propagate(clauses, assignment)
        if clauses is None:
            return False
        if not clauses:
            return True
        
        pure_literals = self.find_pure_literals(clauses)
        if pure_literals:
            for literal in pure_literals:
                assignment[literal] = True
            new_clauses = self.simplify_clauses(clauses, pure_literals)
            return self.dpll(new_clauses, assignment)

        # Choose a literal (splitting)
        literal = self.choose_literal(clauses)
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if self.dpll(self.simplify_clauses(clauses, [literal]), new_assignment):
            return True
        new_assignment = assignment.copy()
        new_assignment[Negation(literal)] = True
        return self.dpll(self.simplify_clauses(clauses, [Negation(literal)]), new_assignment)
        
    def unit_propagate(self, clauses:set[Sentence], assignment):
        while True:
            unit_clauses = [c for c in clauses if self.is_unit_clause(c)]
            if not unit_clauses:
                break
            for unit in unit_clauses:
                literal = unit.arg if isinstance(unit, Negation) else unit
                if isinstance(literal, Negation):
                    assignment[literal.arg] = False
                else:
                    assignment[literal] = True
                clauses = self.simplify_clauses(clauses, [literal])
                if not clauses:
                    return None, assignment
        return clauses, assignment
    
    def is_unit_clause(self, clause):
        return \
            isinstance(clause, Symbol) or \
            (
                isinstance(clause, Negation) and \
                isinstance(clause.arg, Symbol)
            )
        
    def find_pure_literals(self, clauses:set[Sentence]):
        literals = set()
        for clause in clauses:
            for symbol in clause.symbols():
                negative = Negation(symbol)
                if self.has_literal(clause, symbol) and not self.has_literal(clause, negative):
                    literals.add(symbol)
                elif self.has_literal(clause, negative) and not self.has_literal(clause, symbol):
                    literals.add(negative)
        return literals
    
    def has_literal(self, clause:Sentence, literal:Symbol|Negation):
        if clause == literal:
            return True
        if isinstance(clause, CommutativeSentence):
            return any(self.has_literal(arg, literal) for arg in clause.args)
        if isinstance(clause, Implication):
            return self.has_literal(clause.antecedent, literal) or self.has_literal(clause.consequent, literal)
        return False
    
    def simplify_clauses(self, clauses:set[Sentence], literals:set[Symbol|Negation]):
        new_clauses = set()
        for clause in clauses:
            if any(self.has_literal(clause, literal) for literal in literals):
                continue
            new_clause = clause
            for literal in literals:
                new_clause = self.simplify_clause(new_clause, literal)
            new_clauses.add(new_clause)
        return new_clauses
    
    def simplify_clause(self, clause:Sentence, literal:Symbol|Negation):
        if clause == literal:
            return Symbol('True')
        if isinstance(clause, Negation) and clause.arg == literal:
            return Symbol('True')
        if isinstance(clause, Disjunction):
            new_args = [arg for arg in clause.args if arg != literal and arg != literal.negate()]
            if not new_args:
                return Symbol('False')
            if len(new_args) == 1:
                return new_args[0]
            return Disjunction(*new_args)
        return clause
    
    def choose_literal(self, clauses:set[Sentence]):
        for clause in clauses:
            if isinstance(clause, Symbol):
                return clause
            if isinstance(clause, Negation):
                return clause.arg
        return None