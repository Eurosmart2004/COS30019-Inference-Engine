from logic import *
from truthtable import *
from forward_chaining import *
from backward_chaining import *
from sentence_transformers import *
from Resolution import Resolution
from Reader import *


'''Test Function'''
# Read File
# filename = 'data/test_HornKB.txt'
# filename = 'data/test_genericKB_1.txt'
# filename = 'data/test.txt'
# filename = 'data/test1.txt'
# filename = 'data/test_genericKB.txt'
filename = 'data/test9.txt'
# filename = 'test_genericKB_proven.txt' 
# filename = 'test_genericKB_unproven.txt'
# filename = 'test.txt'
# filename = 'test1.txt'
# filename = 'test2.txt'
# filename = 'test3.txt'
# filename = 'test4.txt'
# filename = 'test5.txt'
# filename = 'test6.txt'
# filename = 'test7.txt'
# filename = 'test8.txt'

print(f'Debug filename: {filename}\n')

tell, query = read(filename)
print(f'Tell: {tell}')
print(f'Query/Ask: {query}\n')

# Extract symbol
symbols, sentences = extract_symbols_and_sentences(tell)
print(f'Symbols: {symbols}')
print(f'Sentence: {sentences}\n')


# Resolution
result_resolution = Resolution(sentences, query).solve()
print(f'Result Resolution: {result_resolution}\n')


# Create a TruthTable instance
truth_table = TruthTable(symbols, sentences, query)
entailed_symbols = truth_table.get_entailed_symbols()
print(entailed_symbols)


fc = ForwardChaining(sentences, query)
fc_result = fc.solve()
print(f'Output:\n{fc_result}')

bc = BackwardChaining(sentences, query)
bc_result = bc.solve()
print(f'Output:\n{bc_result}\n')