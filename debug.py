"""
This module is used for debugging purposes. It reads a file containing a knowledge base and a query, and then runs all algorithms on them.
"""

import sys
from syntax import *
from algorithms import *
from parser import parse_kb_and_query


'''Test Function'''
# Read File
file_name = 'test_HornKB.txt'
file_name = 'test_HornKB_2.txt'
file_name = 'test_HornKB_3.txt'
file_name = 'test_genericKB_1.txt'
file_name = 'test.txt'
file_name = 'test1.txt'
file_name = 'test_genericKB.txt'
file_name = 'test9.txt'
file_name = 'test_genericKB_proven.txt' 
file_name = 'test_genericKB_unproven.txt'
file_name = 'test.txt'
# file_name = 'test1.txt'
# file_name = 'test2.txt'
# file_name = 'test3.txt'
# file_name = 'test4.txt'
# file_name = 'test5.txt'
# file_name = 'test6.txt'
# file_name = 'test7.txt'
# file_name = 'test8.txt'

print(f'Debug file_name: {file_name}\n')

kb, query = parse_kb_and_query(file_name)
print(f"Knowledge Base / Tell: {kb}")
# print(f"Arguments: {[type(clause) for clause in kb.args]}")
print(f"Query / Ask: {query}")

# Truth Table
print("\nTruth Table:")
tt = TruthTable(kb, query)
tt.solve()
sys.stdout.reconfigure(encoding='utf-8')
table = tt.generate_table()
# print(table)

# Forward Chaining
print("\nForward Chaining:")
fc = ForwardChaining(kb, query)
fc.solve()

# Backward Chaining
print("\nBackward Chaining:")
bc = BackwardChaining(kb, query)
bc.solve()

# Resolution
print("\nResolution:")
resolution = Resolution(kb, query)
resolution.solve()

# DPLL
print("\nDPLL:")
dpll = DPLL(kb, query)
dpll.solve()