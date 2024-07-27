import sys
from Reader import read, extract_symbols_and_sentences
from truthtable import TruthTable
from backward_chaining import BackwardChaining
from forward_chaining import ForwardChaining
from Resolution import Resolution

def main(method, filename):
    # Read File
    tell, query = read(filename)

    # Extract symbol
    symbols, sentences = extract_symbols_and_sentences(tell)

    # Output the results
    print('Results:')

    if method == "TT":
    # Create a TruthTable instance
        # truth_table = TruthTable(symbols, knowledge_base, query_sentence)
        truth_table = TruthTable(symbols, sentences, query)
        entailed_symbols = truth_table.get_entailed_symbols()
        print(entailed_symbols)
        print(truth_table)
    elif method == "FC":
    # Forward Chaining
        fc = ForwardChaining(sentences, query)
        fc_result = fc.solve()
        print(fc_result)
    elif method == "BC":
    # Backward Chaining
        bc = BackwardChaining(sentences, query)
        bc_result = bc.solve()
        print(bc_result)
    elif method == "RES":
    # Resolution
        result_resolution = Resolution(sentences, query).solve()
        print(result_resolution)

if __name__ == "__main__":
    method = sys.argv[1]
    filename = sys.argv[2]
    main(method, filename)
