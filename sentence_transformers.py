import re
from truthtable import *
from logic import *
from typing import List, Union

class Parser:
    def __init__(self, input):
        self.input = input
        self.position = 0

    def consume_whitespace(self):
        while self.position < len(self.input) and self.input[self.position].isspace():
            self.position += 1

    def match(self, string):
        self.consume_whitespace()
        if self.input.startswith(string, self.position):
            self.position += len(string)
            return True
        return False

    def parse_symbol(self):
        self.consume_whitespace()
        start_position = self.position
        while self.position < len(self.input) and self.input[self.position].isalnum():
            self.position += 1
        return Symbol(self.input[start_position:self.position])

    def parse_atom(self):
        if self.match("("):
            result = self.parse_biconditional()
            if not self.match(")"):
                raise Exception("Expected ')'")
            return result
        else:
            return self.parse_symbol()

    def parse_negation(self):
        if self.match("~"):
            return Negation(self.parse_atom())
        else:
            return self.parse_atom()

    def parse_conjunction(self):
        result = self.parse_negation()
        while self.match("&"):
            result = Conjunction(result, self.parse_negation())
        return result

    def parse_disjunction(self):
        result = self.parse_conjunction()
        while self.match("||"):
            result = Disjunction(result, self.parse_conjunction())
        return result

    def parse_implication(self):
        result = self.parse_disjunction()
        while self.match("=>"):
            result = Implication(result, self.parse_disjunction())
        return result

    def parse_biconditional(self):
        result = self.parse_implication()
        while self.match("<=>"):
            result = Biconditional(result, self.parse_implication())
        return result

    def parse(self):
        return self.parse_biconditional()


class ParseCNF():
    def __init__(self, input: Union[str, Sentence]):
        self.input = input

    def parse(self):
        if isinstance(self.input, str):
            self.sentence = Parser(self.input).parse()
        else:
            self.sentence = self.input
        # Convert the sentence to CNF
        cnf = self.to_cnf(self.sentence)
        cnf_list = []
        if isinstance(cnf, Conjunction):
            for arg in cnf.conjuncts():
                if isinstance(arg, Disjunction):
                    resolve = self.resolve_disjunction(arg)
                    if resolve != None: cnf_list.append(resolve)
                else:
                    cnf_list.append(arg)
            return Conjunction(*cnf_list)
        else:
            return cnf
                
    def to_cnf(self, node):
        if isinstance(node, Biconditional):
            return Conjunction(self.to_cnf(Implication(node.args[0], node.args[1])), self.to_cnf(Implication(node.args[1], node.args[0])))
        
        elif isinstance(node, Implication):
            return Disjunction(Negation(self.to_cnf(node.args[0])), self.to_cnf(node.args[1]))
        
        elif isinstance(node, Conjunction):
            conjunction_args = []
            for arg in node.args:
                cnf_arg = self.to_cnf(arg)
                if isinstance(cnf_arg, Conjunction):
                    conjunction_args.extend(cnf_arg.args)
                else:
                    conjunction_args.append(cnf_arg)
            return Conjunction(*conjunction_args)
        
        elif isinstance(node, Disjunction):
            disjunction_args = []
            conjunctions = []
            for arg in node.args:
                cnf_arg = self.to_cnf(arg)
                if isinstance(cnf_arg, Disjunction):
                    disjunction_args.extend(cnf_arg.args)
                elif isinstance(cnf_arg, Conjunction):
                    conjunctions.append(cnf_arg)
                else:
                    disjunction_args.append(cnf_arg)
            if conjunctions:
                conj = []
                distribute = self.distribute_or_over_and(conjunctions, disjunction_args)
                conj.extend(distribute.args)
                return Conjunction(*conj)
            else:
                return Disjunction(*disjunction_args)
        
        elif isinstance(node, Negation):
            return self.move_not_inwards(node)
        
        else:  # node is a Symbol
            return node
        
    def distribute_or_over_and(self, conjunctions, disjunctions):
        new_nodes = []
        if len(conjunctions) > 1:
            # Distribute OR over AND for all conjunctions
            for i in range(len(conjunctions)):
                for arg1 in conjunctions[i].args:
                    for j in range(i+1, len(conjunctions)):
                        for arg2 in conjunctions[j].args:
                            new_nodes.append(Disjunction(arg1, arg2))
        elif len(conjunctions) == 1:
            # If there's only one conjunction, just add its arguments to new_nodes
            new_nodes.extend(conjunctions[0].args)
        # At this point, all conjunctions have been distributed.
        # Now we distribute the disjunctions over the result.
        final_nodes = []
        if len(disjunctions) > 0:
            for node in new_nodes:
                for disj in disjunctions:
                    if isinstance(disj, Disjunction):
                        final_nodes.extend([Disjunction(node, *disj)])
                    else:
                        final_nodes.extend([Disjunction(node, disj)])
        else:
            # If there are no disjunctions, just return the new_nodes as a Conjunction
            return Conjunction(*new_nodes)
        return Conjunction(*final_nodes)

    def move_not_inwards(self, node):
        # Move NOT inwards
        if isinstance(node.args[0], Negation):
            if isinstance(node.args[0].args[0], Symbol):
                return node.args[0].args[0]  # return the symbol if it's a negation of a negation of a symbol
            else:
                return self.to_cnf(node.args[0].args[0])
            
        elif isinstance(node.args[0], Conjunction):
            new_args = []
            for arg in node.args[0].args:
                cnf_arg = self.to_cnf(arg)
                if not isinstance(cnf_arg, Symbol):
                    new_arg = self.to_cnf(self.move_not_inwards(Negation(cnf_arg)))
                else:
                    new_arg = Negation(cnf_arg)
                new_args.append(new_arg)
            return Disjunction(*new_args)
        
        elif isinstance(node.args[0], Disjunction):
            new_args = []
            for arg in node.args[0].args:
                cnf_arg = self.to_cnf(arg)
                if not isinstance(cnf_arg, Symbol):
                    new_arg = self.to_cnf(self.move_not_inwards(Negation(cnf_arg)))
                else:
                    new_arg = Negation(cnf_arg)
                new_args.append(new_arg)
            return Conjunction(*new_args)
        
        else:
            return node

    def resolve_disjunction(self, node):
        if isinstance(node, Disjunction):
            literals = node.args
            resolved_literals = []
            for literal1 in literals:
                for literal2 in literals:
                    if isinstance(literal1, Negation) and literal1.args[0] == literal2:
                        resolved_literals.append(literal1)
                        resolved_literals.append(literal2)
                    elif isinstance(literal2, Negation) and literal2.args[0] == literal1:
                        resolved_literals.append(literal1)
                        resolved_literals.append(literal2)
            remaining_literals = [l for l in literals if l not in resolved_literals]
            if remaining_literals:
                return Disjunction(*remaining_literals)
            else:
                return None
        else:
            return node

    
def parse(sentence):
    return Parser(sentence).parse()

def parse_cnf(sentence):
    return ParseCNF(sentence).parse()

def create_knowledge_base(sentences):
    parsed_sentences = []
    for sentence in sentences:
        parsed_sentence = parse(sentence.strip())
        parsed_sentences.append(parsed_sentence)
    knowledge_base = Conjunction(*parsed_sentences)
    return knowledge_base


if __name__ == "__main__":
    # Test the parser
    # Test 1
    # Input: (A & B) => C
    # Output: Implication(Conjunction(Symbol('A'), Symbol('B')), Symbol('C'))
    print(parse("t<=>s=>r||q&~p"))
    print(parse("(A & B) => C"))

    # Test 2
    # Input: A & B & C
    # Output: Conjunction(Symbol('A'), Symbol('B'), Symbol('C'))
    print(parse("A & B & C"))

    # Test 3
    # Input: A | B | C
    # Output: Disjunction(Symbol('A'), Symbol('B'), Symbol('C'))
    print(parse("A || B || C"))

    # Test 4
    # Input: A <=> B
    # Output: Conjunction(Implication(Symbol('A'), Symbol('B')), Implication(Symbol('B'), Symbol('A')))
    print(parse("A <=> B"))

    # Test 5
    # Input: ~A
    # Output: Negation(Symbol('A'))
    print(parse("~A"))

    # Test 6
    # Input: ~(A | B)
    # Output: Negation(Disjunction(Symbol('A'), Symbol('B')))
    print(parse("~(A || B)"))

    # Test 7
    # Input: ~(A & B)
    # Output: Negation(Conjunction(Symbol('A'), Symbol('B')))
    print(parse("~(A & B)"))

    # Test 8
    # Input: A & B | C
    # Output: Disjunction(Conjunction(Symbol('A'), Symbol('B')), Symbol('C'))
    print(parse("A & B || C"))

    # Test 9
    # Input: A | B & C
    # Output: Disjunction(Symbol('A'), Conjunction(Symbol('B'), Symbol('C')))
    print(parse("A || B & C"))

    # Test 10
    # Input: A & B | C & D
    # Output: Disjunction(Conjunction(Symbol('A'), Symbol('B')), Conjunction(Symbol('C'), Symbol('D')))
    print(parse("A & B || C & D"))

    # Test 11
    # Input: A & B | C | D
    # Output: Disjunction(Conjunction(Symbol('A'), Symbol('B')), Symbol('C'),
    
    