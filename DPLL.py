from logic import Symbol, Negation, Disjunction, Conjunction
from sentence_transformers import parse_cnf
from typing import List
class DPLL:
    def __init__(self, sentences: List[str], query: str):
        self.knowledge_base = self.process(sentences, query)

    def process(self, sentences: List[str], query: str):
        parsed_sentences = [parse_cnf(sentence) for sentence in sentences]
        query = parse_cnf(query)
        knowledge_base = Conjunction(*parsed_sentences, query)
        return parse_cnf(knowledge_base)

    def solve(self):
        symbols = self.knowledge_base.symbols()
        return self.dpll(self.knowledge_base, symbols, {})

    def dpll(self, clauses: Conjunction, symbols: dict, model: dict):
        if not symbols:
            return clauses.evaluate(model)

        # Choose a symbol from symbols
        p, rest = symbols.pop(), symbols

        # Try assigning the current symbol to True and False, and backtrack if necessary
        model1 = model.copy()
        model1[p] = True
        result_true = self.dpll(clauses, rest.copy(), model1)
        if result_true:
            return True

        model2 = model.copy()
        model2[p] = False
        return self.dpll(clauses, rest.copy(), model2)