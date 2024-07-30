import sys, os
# from itertools import product
from tabulate import tabulate

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from syntax import *
from parser import parse_kb_and_query


class TruthTable:
    def __init__(self, kb: Conjunction, query: Sentence):
        self.kb = kb
        self.query = query
        self.symbols = sorted(kb.symbols() | query.symbols(), key=lambda x: x.name)
        self.table = []
        self.valid_models_count = 0

    def solve(self):
        model = {}
        valid = self.check_all(self.kb, self.query, self.symbols, model)
        if valid and self.valid_models_count > 0:
            print(f'YES: {self.valid_models_count}')
        else:
            print('NO')

    def check_all(self, kb: Conjunction, query: Sentence, symbols: set[Symbol], model: dict):
        if not symbols:
            kb_eval = kb.evaluate(model)
            query_eval = query.evaluate(model)
            self.table.append((model.copy(), kb_eval, query_eval))
            if kb_eval and query_eval:
                self.valid_models_count += 1
        else:
            symbol, *rest = symbols
            return all([
                self.check_all(kb, query, rest, {**model, symbol: True}),
                self.check_all(kb, query, rest, {**model, symbol: False})
            ])

    def generate_table(self):        
        headers = [symbol for symbol in self.symbols] 
        headers += ['KB: ' + str(self.kb), 'Query: ' + str(self.query)]
        rows = []
        for model, kb_eval, query_eval in self.table:
            row = [str(model[symbol]) for symbol in self.symbols] + [str(kb_eval), str(query_eval)]
            rows.append(row)
        # print(len(headers), len(rows[0]))
        return tabulate(rows, headers, tablefmt='fancy_grid')
     
    
if __name__ == "__main__":
    # file_name = 'test_genericKB.txt'
    file_name = 'test9.txt'
    kb, query = parse_kb_and_query(file_name)
    print(f"Knowledge Base: {kb}")
    print(f"Query: {query}")
    
    tt = TruthTable(kb, query)
    tt.solve()
    sys.stdout.reconfigure(encoding='utf-8')
    table = tt.generate_table()
    print(table)