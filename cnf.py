from syntax import *

def to_cnf(sentence: Sentence):
    # Convert to Negation Normal Form (NNF) first
    nnf = _to_nnf(sentence)
    # Then convert NNF to CNF
    cnf = _distribute_or_over_and(nnf)
    # Resolve Disjunctions in the result
    return _resolve_disjunction(cnf)

def _to_nnf(sentence: Sentence):
    if isinstance(sentence, Symbol):
        return sentence
    elif isinstance(sentence, Negation):
        return _move_not_inwards(sentence)
        
    elif isinstance(sentence, Conjunction):
        return Conjunction(*[_to_nnf(arg) for arg in sentence.args])
    
    elif isinstance(sentence, Disjunction):
        return Disjunction(*[_to_nnf(arg) for arg in sentence.args])
    
    elif isinstance(sentence, Implication):
        return _to_nnf(Disjunction(Negation(sentence.antecedent), sentence.consequent))
    
    elif isinstance(sentence, Biconditional):
        arg_1, arg_2 = sentence.args
        return Conjunction(_to_nnf(Implication(arg_1, arg_2)), 
                           _to_nnf(Implication(arg_2, arg_1)))
        
def _move_not_inwards(sentence: Negation):
    # print(sentence)
    if isinstance(sentence.arg, Symbol):
        return sentence
    elif isinstance(sentence.arg, Negation):
        return _to_nnf(sentence.arg.arg)
    elif isinstance(sentence.arg, Conjunction):
        return Disjunction(*[_to_nnf(Negation(arg)) for arg in sentence.arg.args])
    elif isinstance(sentence.arg, Disjunction):
        return Conjunction(*[_to_nnf(Negation(arg)) for arg in sentence.arg.args])
    elif isinstance(sentence.arg, Implication):
        return Conjunction(_to_nnf(sentence.arg.antecedent), _to_nnf(Negation(sentence.arg.consequent)))
    

def _distribute_or_over_and(sentence: Sentence):
    if isinstance(sentence, Disjunction):
        if any(isinstance(arg, Conjunction) for arg in sentence.args):
            conj = next(arg for arg in sentence.args if isinstance(arg, Conjunction))
            others = [arg for arg in sentence.args if arg is not conj]
            return Conjunction(*[_distribute_or_over_and(Disjunction(*(others + [arg]))) for arg in conj.args])
        else:
            return sentence
    elif isinstance(sentence, Conjunction):
        return Conjunction(*[_distribute_or_over_and(arg) for arg in sentence.args])
    else:
        return sentence

def _resolve_disjunction(sentence: Sentence):
    if isinstance(sentence, Conjunction):
        return Conjunction(*[_resolve_disjunction(arg) for arg in sentence.args])
    elif isinstance(sentence, Disjunction):
        resolved_args = []
        for arg in sentence.args:
            if not any(_is_complementary(arg, other) for other in sentence.args if other is not arg):
                resolved_args.append(arg)
        if len(resolved_args) == 0:
            return Symbol("True")
        return Disjunction(*resolved_args)
    else:
        return sentence
    
def _is_complementary(arg_1: Sentence, arg_2: Sentence):
    return arg_1 == arg_2 \
        or isinstance(arg_1, Negation) and arg_1.arg == arg_2 \
        or isinstance(arg_2, Negation) and arg_2.arg == arg_1