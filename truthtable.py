from itertools import product
from tabulate import tabulate
from typing import List, Union
from logic import Symbol
from sentence_transformers import create_knowledge_base, parse

class TruthTable:
    def __init__(self, symbols: Symbol, sentences: List[str], query: str):
        self.knowledge_base = create_knowledge_base(sentences)
        self.query = parse(query)
        self.symbols = sorted(symbols)
        self.table = self.generate_table()
        self.count = 0

    def model_check(knowledge, query):
        """Checks if knowledge base entails query."""

        def check_all(knowledge, query, symbols, model):
            """Checks if knowledge base entails query, given a particular model."""

            # If model has an assignment for each symbol
            if not symbols:

                # If knowledge base is true in model, then query must also be true
                if knowledge.evaluate(model):
                    return query.evaluate(model)
                return True
            else:

                # Choose one of the remaining unused symbols
                remaining = symbols.copy()
                p = remaining.pop()

                # Create a model where the symbol is true
                model_true = model.copy()
                model_true[p] = True

                # Create a model where the symbol is false
                model_false = model.copy()
                model_false[p] = False

                # Ensure entailment holds in both models
                return (check_all(knowledge, query, remaining, model_true) and
                        check_all(knowledge, query, remaining, model_false))

        # Get all symbols in both knowledge and query
        symbols = set.union(knowledge.symbols(), query.symbols())

        # Check that knowledge entails query
        return check_all(knowledge, query, symbols, dict())

    def generate_table(self):
        combinations = list(product([True, False], repeat=len(self.symbols)))
        models = [{symbol: value for symbol, value in zip(self.symbols, combination)} for combination in combinations]
        evaluations = [[self.knowledge_base.evaluate(model)] for model in models]
        return list(zip(models, evaluations))

    def check_facts(self):
        for model, evaluation in self.table:
            if all(evaluation) and self.query.evaluate(model):
                self.count += 1
        return False
    
    def brute_force_check(self):
        is_Valid = self.model_check(self.knowledge_base, self.query)
        return is_Valid
    

    def get_entailed_symbols(self):
        self.check_facts()
        valid = self.brute_force_check()

        if self.count > 0 and valid:
            return f'YES: {self.count}'
        else:
            return f'NO {self.query} cannot be proven'
        
    def __str__(self):
        headers = [str(symbol) for symbol in self.symbols]
        headers += [str(self.knowledge_base)] + [str(self.query)]

        rows = []
        for model, evaluations in self.table:
            row = [str(model[symbol]) for symbol in self.symbols]
            row += [str(evaluations[0])] + [str(self.query.evaluate(model))]
            rows.append(row)

        return tabulate(rows, headers, tablefmt='fancy_grid')