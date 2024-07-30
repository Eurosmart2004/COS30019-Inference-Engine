import sys, os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from syntax import *
from parser import parse_kb_and_query


class ForwardChaining:
    def __init__(self, kb: Conjunction, query: Symbol):
        self.kb = kb
        self.query = query
        self.check_kb()
        self.check_query()
    
    def solve(self):
        # Initialize the agenda with symbols known to be true
        agenda = [symbol for symbol in self.kb.args if isinstance(symbol, Symbol)]
        agenda.sort(key=lambda x: x.name)
        # print(agenda)
        
        # Initialize inferred and count dictionaries
        inferred = {symbol: False for symbol in self.kb.symbols()}
        count = {}
        
        for clause in self.kb.args:
            if isinstance(clause, Implication):
                count[clause] = len(clause.antecedent.symbols())
        # print(count)
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
        
    def check_kb(self):
        for clause in kb.args:
            if not isinstance(clause, (Implication, Symbol)):
                print("Warning: Knowledge base is not in Horn form. The algorithm may not function correctly.")
                return False
        return True
    
    def check_query(self):
        if not isinstance(self.query, Symbol):
            print("Warning: Query is not a symbol. The algorithm may not function correctly.")
            return False
        return True
     
    
if __name__ == "__main__":
    # file_name = 'test_genericKB.txt'
    file_name = 'test_HornKB.txt'
    kb, query = parse_kb_and_query(file_name)
    print(f"Knowledge Base: {kb}")
    print(f"Query: {query}")
    
    fc = ForwardChaining(kb, query)
    fc.solve()