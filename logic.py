class Sentence:   
    # Logical sentence
    def __init__(self, *args):
        self.args = args

    # Sub class implement
    def evaluate(self, model):
        pass
    
    # Sub class implement
    def symbols(self):
        return set()

class Symbol(Sentence):
    
    # Logical proposition with a specific truth value
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name
    
    def __eq__(self, other):
        if isinstance(other, Symbol):
            return self.name == other.name
        return False
    
    def __hash__(self):
        return hash(self.name)

    # Evaluates the truth value in model
    def evaluate(self, model):
        try:
            return bool(model[self.name])
        except KeyError:
            raise Exception(f"variable {self.name} not in model")

    # Return set of symbol
    def symbols(self):
        return {self.name}

class Negation(Sentence):
    # Negation = Not | Symbol ~
    # Logical Negation
    def __repr__(self):
        if isinstance(self.args[0], Symbol):
            return f'~{self.args[0]}'
        else:
            return f'~({self.args[0]})'
        
    def __hash__(self):
        return hash(self.args)
        
    def __eq__(self, other):
        if isinstance(other, Negation):
            return self.args == other.args
        return False

    # Evaluates the Negation value in model
    def evaluate(self, model):
        return not self.args[0].evaluate(model)

    # Return symbols in Negation
    def symbols(self):
        return self.args[0].symbols()

class Conjunction(Sentence):
    # Conjunction = And | Symbol &
    # Logical Conjunction

    def __init__(self, *args):
        self.args = tuple(set(args))

    def __repr__(self):
        return ' & '.join((f"({str(arg)})" if not isinstance(arg, (Symbol, Negation)) else str(arg)) for arg in self.args)
    
    def __eq__(self, other):
        if isinstance(other, Conjunction):
            return self.args == other.args
        return False
    
    def __hash__(self):
        return hash(self.args)

    # Evaluates the Conjunction value in model
    def evaluate(self, model):
        return all(arg.evaluate(model) for arg in self.args)
    
    # Return symbols in Conjunction
    def symbols(self):
        return set.union(*[arg.symbols() for arg in self.args])
    
    def conjunct_premise(self, conjunct):
            return conjunct.args[0].symbols()
    
    def conjuncts(self):
        return [arg for arg in self.args]
    
    def conjunct_conclusion(self, conjunct):
        return conjunct.args[1].symbols().pop()


    # Debug Function
    def print_arg_types(self):
        for arg in self.args:
            print(type(arg))
        
class Disjunction(Sentence):
    # Disjunction = Or | Symbol ||
    # Logical Disjunction
    def __init__(self, *args):
        # self.args = args
        self.args = tuple(set(args))

    def __repr__(self):
        return ' || '.join((f"({str(arg)})" if not isinstance(arg, (Symbol, Negation)) else str(arg)) for arg in self.args)
    
    def __eq__(self, other):
        if isinstance(other, Disjunction):
            return self.args == other.args
        return False

    def __hash__(self):
        return hash(self.args)

    # Evaluates the Disjunction value in model
    def evaluate(self, model):
        return any(arg.evaluate(model) for arg in self.args)

    def disjuncts(self):
        return [arg for arg in self.args]

    # Return symbols in Disjunction
    def symbols(self):
        return set.union(*[arg.symbols() for arg in self.args])
    

class Implication(Sentence):
    # Symbol =>
    # Logical Implication
    def __repr__(self):
        return f'({self.args[0]} => {self.args[1]})'
    
    def __eq__(self, other):
        if isinstance(other, Implication):
            return self.args == other.args
        return False

    def __hash__(self):
        return hash(self.args)

    # Evaluates the Implication value in model
    def evaluate(self, model):
        return not self.args[0].evaluate(model) or self.args[1].evaluate(model)

    # Return symbols in Implication
    def symbols(self):
        return set.union(*[arg.symbols() for arg in self.args])
    
    # Debug Function
    def print_arg_types(self):
        print(f"{type(self.args[0])} => {type(self.args[1])}")

class Biconditional(Sentence):
    # Symbol <=>
    # Logical Bicondition
    def __repr__(self):
        return f'({self.args[0]} <=> {self.args[1]})'
    
    def __eq__(self, other):
        if isinstance(other, Biconditional):
            return self.args == other.args
        return False
    
    def __hash__(self):
        return hash(self.args)

    # Evaluates the Bicondition value in model
    def evaluate(self, model):
        return self.args[0].evaluate(model) == self.args[1].evaluate(model)

    # Return symbols in Bicondition
    def symbols(self):
        return set.union(*[arg.symbols() for arg in self.args])

