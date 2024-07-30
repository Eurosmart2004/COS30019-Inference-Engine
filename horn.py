from syntax import *


def check_horn_query(query: Sentence) -> bool:
    if not isinstance(query, Symbol):
        print("Warning: Query is not a symbol. The algorithm may not function correctly.")


def check_horn_kb(kb: Conjunction) -> bool:
    if not all(_is_horn_form(clause) for clause in kb.args):
        # print(kb.args)
        print("Warning: Knowledge base is not in Horn form. The algorithm may not function correctly.")
    
    
def _is_horn_form(clause: Sentence) -> bool:
    if isinstance(clause, Symbol):
        return True
    if isinstance(clause, Negation) and isinstance(clause.arg, Symbol):
        return True
    if isinstance(clause, Disjunction):
        positive_symbols = [arg for arg in clause.args if isinstance(arg, Symbol)]
        return len(positive_symbols) <= 1 and \
            all(isinstance(arg, (Symbol, Negation)) for arg in clause.args)
    if isinstance(clause, Implication):
        if not isinstance(clause.consequent, Symbol):
            return False
        if isinstance(clause.antecedent, Symbol):
            return True
        if isinstance(clause.antecedent, Conjunction):
            return all(isinstance(arg, Symbol) for arg in clause.antecedent.args)
    # if isinstance(clause, Conjunction):
    #     return all(_is_horn_form(arg) for arg in clause.args)
    return False