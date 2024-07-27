from sentence_transformers import ParseCNF, parse_cnf
from logic import Negation, Disjunction, Conjunction
from copy import copy
class Resolution:
    def __init__(self, sentences, query):
        self.knowledge_base = self.process(sentences, query)

    def process(self, sentences: str, query: str):
        parsed_sentences = [parse_cnf(sentence) for sentence in sentences]
        query = Negation(parse_cnf(query))
        # Parse again to avoid nested negations
        query = parse_cnf(query)
        knowledge_base = Conjunction(*parsed_sentences, query)
        return parse_cnf(knowledge_base)

    def solve(self):
        while True:
            new_clauses = []
            kb = self.knowledge_base.conjuncts() if isinstance(self.knowledge_base, Conjunction) else [self.knowledge_base]
            for clause1 in kb:
                for clause2 in kb:
                    if clause1 != clause2:
                        resolvents = self.resolve(clause1, clause2)
                        if len(resolvents.args) == 0:
                            return True
                        new_clauses.append(resolvents)

            if  len(new_clauses) == 0 or self.is_subset(new_clauses, kb):
                return False
            for clause in new_clauses:
                if clause not in kb:
                    kb.append(clause)
            self.knowledge_base = Conjunction(*kb)

    def resolve(self, clause1, clause2):
        literals1 = clause1.disjuncts() if isinstance(clause1, Disjunction) else [clause1]
        literals2 = clause2.disjuncts() if isinstance(clause2, Disjunction) else [clause2]
        for literal1 in literals1:
            for literal2 in literals2:
                if isinstance(literal1, Negation) and literal1.args[0] == literal2:
                    return  Disjunction(*[l for l in literals1 if l != literal1], *[l for l in literals2 if l != literal2])
                elif isinstance(literal2, Negation) and literal2.args[0] == literal1:
                    return Disjunction(*[l for l in literals1 if l != literal1], *[l for l in literals2 if l != literal2])
                
        return Disjunction(clause1, clause2)

    def is_subset(self, set1, set2):
        return all(element in set2 for element in set1)