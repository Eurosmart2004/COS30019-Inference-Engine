import sys, os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from syntax import *
from horn import check_horn_kb, check_horn_query


class ForwardChaining:
    def __init__(self, kb: Conjunction, query: Symbol):
        self.kb = kb
        self.query = query
        check_horn_kb(self.kb)
        check_horn_query(self.query)
    
    def solve(self):
        # Initialize inferred and count dictionaries
        inferred = {symbol: False for symbol in self.kb.symbols()}
        count = {}
        
        # Initialize the agenda with symbols known to be true
        if isinstance(self.kb, Symbol):
            agenda = [self.kb]
        elif isinstance(self.kb, Implication):
            agenda = []
            count[self.kb] = len(self.kb.antecedent.symbols())
        else: # Conjunction
            agenda = [symbol for symbol in self.kb.args if isinstance(symbol, Symbol)]
            for clause in self.kb.args:
                if isinstance(clause, Implication):
                    count[clause] = len(clause.antecedent.symbols())
            # print(count)
        agenda.sort(key=lambda x: x.name)
        # print(agenda)        
        
        chain:list[Symbol] = []  # Track the result of forward chaining
        
        while agenda:
            p = agenda.pop(0)
            chain.append(p)
            if p == self.query:
                print(f"YES: {', '.join([symbol.name for symbol in chain])}")
                return
            # print(p, type(p), inferred)
            if not inferred[p]:
                inferred[p] = True
                for clause in self.kb.args:
                    if isinstance(clause, Implication):
                        if p in clause.antecedent.symbols():
                            # print(clause.antecedent.symbols())
                            count[clause] -= 1
                            if count[clause] == 0:
                                agenda.append(clause.consequent)
        
        print("NO")
     