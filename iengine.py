import sys
from syntax import *
from algorithms import *
from parser import parse_kb_and_query

def main(method, file_name):
    # Parse the knowledge base and query from the file
    kb, query = parse_kb_and_query(file_name)

    # Based on the method, create the appropriate object and solve
    if method == "TT":
        # Truth Table
        solver = TruthTable(kb, query)
    elif method == "FC":
        # Forward Chaining
        solver = ForwardChaining(kb, query)
    elif method == "BC":
        # Backward Chaining
        solver = BackwardChaining(kb, query)
    elif method == "RES":
        # Resolution
        solver = Resolution(kb, query)
    elif method == "DPLL":
        # DPLL
        solver = DPLL(kb, query)
    else:
        print("Invalid method")
        return
    
    print()
    solver.solve()
    print()
    

if __name__ == "__main__":
    method = sys.argv[1]
    filename = sys.argv[2]
    main(method, filename)
